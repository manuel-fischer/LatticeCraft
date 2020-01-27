import os
import fileFactory

if __name__ == "__main__":
    os.chdir("./dis_game")
    fileFactory.bake("blueprint.txt", "../game.tscript")
    os.chdir("..")
