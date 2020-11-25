When adding blocks, you might want to introduce unique textures for the block.
This is done by writing a function, that takes a single parameter, a draw object:
The draw object is a simplified version of the canvas namspace, it only provides
a subset of its functions: `scale, setFillColor, fillRect`. These work exactly
like the `canvas` counterparts.

The texture is applied to a block by simply creating the block with a parameter that is
the drawing function.

```
#[file] mod.tscript#textures
function drawRedBlock(draw)
{
	draw.scale(1/16); # dividing up into 16 by 16 pixels
	draw.setFillColor(0.5, 0, 0);
	draw.fillRect(0, 0, 16, 16);
	draw.setFillColor(1, 0, 0);
	draw.fillRect(1, 1, 14, 14);
}
#[file] mod.tscript#blocks
var RED_BLOCK = Block("R", drawRedBlock);
```

See mod_blocks.md for adding blocks.