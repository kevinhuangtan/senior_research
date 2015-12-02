HaloTools API
====================

Quick dictionary-like access to any tree's halo property data
---------------------

### Usage

1) Place subvolume file (e.g. tree_0_0_0.dat) in tree_ascii_data/<br>
2) Build data for new subvolume<br>

	>>> #example
	>>> from build_subvolume import build
	>>> build("0_0_0")

retrieve trunk data for mvir of a given tree: <br>

	>>> import haloprop
	>>> treeID = '3060299107' #tree ID in tree_0_0_0.dat subvolume
	>>> haloprop_key = 'mvir'
	>>> print haloprop.get_trunk_haloprop(treeID, haloprop_key)

retrieve clumpiness summary statistic for a tree ID <br>

	>>> import haloprop
	>>> treeID = '3060299107' #tree ID in tree_0_0_0.dat subvolume
	>>> print haloprop.clumpiness(treeID)
	>>> "clumpiness:  0.0974984867952"