import subvolume_directory
import tree_directory
import haloprop_binary
import numpy as np
import h5py
import advanced_data
from dtype import dt

def build_subvolume(subvolume):
    """
    Converts subvolume ascii file into accesible data via tree ID.

    1) Build binary files for subvolume halo properties.
    properties added: mvir, haloid_next_coprog_depthfirst, haloid_depth_first, upid, scale

    2) Adds tree metadata for each tree in the subvolume to tree directory.
	tree metadata: length, offset, depthfirst ID, lastmainleaf ID of each tree

	3) Adds all tree ID's in the subvolume to the subvolume directory. 
    
    Parameters
    ----------
    subvolume : string
        Name of subvolume

    Examples
    --------
    
    >>> build_subvolume('0_0_0')
    
    """

	haloprops = ['mvir', 'haloid_next_coprog_depthfirst', 'haloid_depth_first', 'upid', 'scale']
	for p in haloprops:
		haloprop_binary.create(subvolume, p)
	tree_directory.create(subvolume)
	subvolume_directory.create(subvolume)


