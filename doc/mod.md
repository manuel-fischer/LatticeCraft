Some of the features might not be implemented in the documented form.

# Modding

## The file structure

It might be helpful to understand the file structure of the sourcecode of LatticeCraft.

The code of LatticeCraft is executed as a single file, but in the directory `dis_game` split up files are available.
Eg. `dis_game/def_blocks.tscript` contains the definitions for different blocks and their behavior. This file is separated into two sections, the definitions section and the behavior section.
These sections appear at different positions in the final source, because the behavior section has additional "external" dependencies, that are by them selves dependent on the definitions section.

The concatenation is done by the command `python asGame.py`. The result is written into `game.tscript`. The contents of that file should then be copied into the TScript IDE.
This large file can be converted back to shorter files by running the command `python disGame.py`. The files in `dis_game` are changed according to the contents of `game.tscript`

Modding is possible by editing the file `dis_game/mod.tscript` or by searching for the string `#[file] mod.tscript` in `game.tscript` and editing the sections accordingly.