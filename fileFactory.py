import sys

COMMENT = "#" # or "//"
COMMENT_SECTION = COMMENT+"[section]"
COMMENT_FILE = COMMENT+"[file]"

BLUEPRINT_COMMENT = "#"
BLUEPRINT_SEP = "#"

class BakingError(BaseException): pass
class UnbakingError(BaseException): pass

def errPrint(*a, **kw):
    print(*a, **kw, file=sys.stderr)

def passFile(filename, mode, function, *a, **kw):
    if filename=="-":
        if "r" in mode:
            return function(sys.stdin, *a, **kw)
        elif "w" in mode:
            return function(sys.stdout, *a, **kw)
    else:
        with open(filename, mode) as f:
            return function(f, *a, **kw)

def parseBlueprint(inp):
    parts = []
    for l in inp.readlines():
        l = l.strip()
        if l.startswith(BLUEPRINT_COMMENT): continue # ignore comments (lines starting with #)
        fnd = l.find(BLUEPRINT_SEP);
        if fnd == -1:
            parts.append((l, "")) # unnamed section, everything before first named
        else:
            parts.append((l[:fnd].rstrip(), l[fnd+len(BLUEPRINT_SEP):].lstrip()))

    return parts

class BakingComponentFile:
    __slots__ = """
        filename
        sections
        sectionsUnused
    """.split()
    
    def __init__(self, fn):
        # parse whole file and search for comments
        self.filename = fn

        self.sections = {}

        curSection = ""
        curContent = ""
        def pushSection():
            nonlocal self, curSection, curContent
            if curSection or curContent:
                self.sections[curSection] = curContent
            curSection = None
            curContent = ""
            
        with open(fn, "rt") as f:
            for i, l in enumerate(f.readlines()):
                ll = l.strip()
                if ll.startswith(COMMENT_SECTION):
                    pushSection()

                    curSection = ll[len(COMMENT_SECTION):].lstrip()
                    if curSection in self.sections:
                        errPrint("%s: line %i: section %s appeared twice"%(fn, i+1, curSection))

                else:
                    curContent += l

        pushSection()


        self.sectionsUnused = list(self.sections.keys())

    def getSectionContent(self, section):
        try: sec = self.sections[section]
        except KeyError:
            errPrint("There is no section", section or "<unnamed>", "in", self.filename)
            raise

        try: self.sectionsUnused.remove(section)
        except ValueError: errPrint("Section", section, "used again")

        return sec

class BakingSession:
    __slots__ = """
        files
    """.split()
    
    def __init__(self):
        self.files = {}


    def getSectionContent(self, fn, section):
        try:
            file = self.files[fn]
        except KeyError:
            file = self.files[fn] = BakingComponentFile(fn)

        return file.getSectionContent(section)
            

    def finish(self):
        for f in self.files.values():
            if f.sectionsUnused:
                errPrint(f.filename + ": Unused sections:")
                for s in sorted(f.sectionsUnused):
                    errPrint("  -", s or "<unnamed>")

def assembleBlueprint(outp, blueprint):
    bs = BakingSession()
    for fn, section in blueprint:
        if COMMENT_FILE:
            if section:
                print(COMMENT_FILE, fn+"#"+section, file=outp)
            else:
                print(COMMENT_FILE, fn, file=outp)
        secContent = bs.getSectionContent(fn, section)
        if secContent[-1:] != "\n": secContent+="\n"
        outp.write(secContent)
        
    bs.finish()

def bake(fnBlueprint, fnOutput):
    blueprint = passFile(fnBlueprint, "rt", parseBlueprint)
    passFile(fnOutput, "wt", assembleBlueprint, blueprint)




class UnbakingComponentFile:
    __slots__ = """
        filename
        content
        sections
    """.split()

    def __init__(self, filename):
        self.filename = filename
        self.content = ""
        self.sections = []

    def putSection(self, section, content):
        while section in self.sections:
            errPrint(self.filename+": Duplicate sections", section)
            section = section + "(%i)"%len(self.sections)

        self.sections.append(section)
        
        if content[-1:] != '\n':
            content += '\n'

        if section:
            self.content += COMMENT_SECTION + " " + section + "\n"
            self.content += content
        else:
            # pull unnamed section to the front
            self.content = content+self.content

        return section
        

class UnbakingSession:
    __slots__ = """
        blueprint
        files
    """.split()
    
    def __init__(self):
        self.blueprint = []
        self.files = {}

    def putSection(self, filename, section, content):
        try:
            file = self.files[filename]
        except KeyError:
            file = self.files[filename] = UnbakingComponentFile(filename)

        section = file.putSection(section, content)
        self.blueprint.append((filename, section))
        


def disassemble(inp):
    bs = UnbakingSession()

    curFileSection = ""
    curContent = ""

    def pushSection():
        nonlocal bs, curFileSection, curContent
        if curFileSection == "": return # move unnamed to first section
        fnd = curFileSection.find("#")
        if fnd == -1:
            curFile = curFileSection
            curSection = ""
        else:
            curFile = curFileSection[:fnd].rstrip()
            curSection = curFileSection[fnd+1:].lstrip()
            
        bs.putSection(curFile, curSection, curContent)
        curContent = ""
    
    for i, l in enumerate(inp.readlines()):
        ll = l.strip()
        if ll.startswith(COMMENT_FILE):
            pushSection()
            curFileSection = ll[len(COMMENT_FILE):].lstrip()
        else:
            curContent += l

    pushSection()
    return bs

    
def createBlueprint(inp, blueprint):
    for fn, section in blueprint:
        fnSection = (fn+BLUEPRINT_SEP+section if section else fn)
        print(fnSection, file=inp)


# writes to files in current working directory
def unbake(fnInput, fnBlueprint):
    unbaked = passFile(fnInput, "rt", disassemble)
    passFile(fnBlueprint, "wt", createBlueprint, unbaked.blueprint)
    for cf in unbaked.files.values():
        # when there are relative path, the unbaking process could lead to writing to
        # other directories, this could be a security problem
        if ".." in cf.filename: raise UnbakingError("Parent directory filenames disabled")
        with open(cf.filename, "wt") as f:
            f.write(cf.content)
            
