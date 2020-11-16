Some of the features might not be implemented in the documented form.

# Generation

The variable `generator` corresponds to the generator of the world. It is possible to extend the generator by adding structures.

## Adding structures

To define a structure, you have to write a function that takes a two parameters, `placer` and `random`.
This function is called, whenever the structure is placed into the world. It might be called multiple times
for the same structure, in this case the function should not have side effects other than on `placer` and `random`.

`placer` has a single member function, `setBlock(x, y, block)`.
The placer object already offsets the coordinate system, so you only have to consider placing blocks around `(0, 0)`.
Usually the origin is at the air block directly above the surface for surface structures.

`random` is an object that has a function also named `random()`, which returns a random number between 0 and 1.
This function should be preferred before using the builtin `math.random()` function,
because of the way the generation works, it is required that your structure generation function always produces the same result,
when called for the same position in the world.

```
function generateBrickColumn(placer, random)
{
	# generate a 3 block tall column of brick blocks
	for var y in 0:3 do
	{
		placer.setBlock(0, y, blocks.brick);
	}
}

generator.addSurfaceStructure(generateBrickColumn, 1, 3);
```

When writing structures you should consider that the ground is not flat, you might add additional dirt and grassblocks around your structure, to give it an additional base.
