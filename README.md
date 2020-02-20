# LatticeCraft
A game written in TScript, similar to Minecraft/Terraria.

## Source Code
[Here](https://raw.githubusercontent.com/manuel-fischer/LatticeCraft/master/game.tscript)

## Gameplay
The main goal is to build your own base, by placing and destroying blocks. Similar to Minecraft your first task is to chop down trees. Use the saplings to regrow the trees. Plant them on dirt or grass; and after little time, a big tree grows again. Use the wood to craft wooden planks in your inventory. So the game should be very familiar to Minecraft players.

## Technical

The world is procedurially generated. This means that the world is indefinite in x-axis and in y-axis. It is possible to save multiple worlds, to be loaded later. When the world is saved, only modified chunks get stored. Those stored chunks get compressed with Run Length Encoding, which merges neighboring blocks of the same type and stores them with a number.

## The Name

The word "Lattice" was chosen, because the regular arrangement of the blocks reminds me (Manuel Fischer) of the crystal lattice structure.
