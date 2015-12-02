HaloTools API
====================

Quick dictionary-like access to any tree's halo property data
---------------------

### Build
Use build.py to build data for any subvolume <br>
example: <br>

	>>> from build import build_subvolume
	>>> import advanced_data
	>>> build_subvolume("0_0_0")
	>>> treeID = '3060299107' #tree ID in tree_0_0_0.dat subvolume
	>>> print advanced_data.clumpiness(treeID)
	>>> "clumpiness:  0.0974984867952"
