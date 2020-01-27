import os
import glob

def tryRemove(f):
    try: os.remove(f)
    except FileNotFoundError: pass

def clean():
    os.chdir("./dis_game")
    tryRemove("blueprint.txt")
    for f in glob.glob("./*.tscript"):
        tryRemove(f)
        #print(f)
    os.chdir("..")
