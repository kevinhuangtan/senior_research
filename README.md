HaloTools API
====================

Quick dictionary-like access to any tree's halo property data
---------------------

### Build
Use build.py to build data for any subvolume <br>
example: <br>

	from build import build_subvolume
	build_subvolume("0_0_0")
	print clumpiness(treeID)
	treeID --> any tree ID in tree_0_0_0.dat subvolume