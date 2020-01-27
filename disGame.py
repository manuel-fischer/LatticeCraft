import os
import fileFactory
import cleanDis

def dis_game():
    os.chdir("./dis_game")
    fileFactory.unbake("../game.tscript", "blueprint.txt")
    os.chdir("..")

if __name__ == "__main__":
    cleanDis.clean()
    dis_game()
    
    
