import os
import numpy as np
import h5py
import matplotlib.pyplot as plt
from build import subvolume_directory, tree_directory, haloprop_binary
from build import dtype


# Tree Directory Metadata
# tree_directory[treeID] = [LENGTH, OFFSET, HALOID_DEPTH_FIRST, HALOID_LAST_MAINLEAF_DEPTHFIRST]

LENGTH = 0
OFFSET = 1
HALOID_DEPTH_FIRST = 2
HALOID_LAST_MAINLEAF_DEPTHFIRST = 3

def get_subvolume(treeID):
    """
    Retrieve tree's subvolume.

    Parameters
    ----------
    treeID : string

    """

    with h5py.File('subvolume_directory.hdf5', "r") as subvol_direc:
        subvolume = subvol_direc[str(treeID)][...][0]
    return subvolume

def get_tree_metadata(treeID):
    """
    Retrieve tree's metadata.

    Parameters
    ----------
    treeID : string

    """
    subvolume = get_subvolume(treeID)
    tree_direc = "trees/"+subvolume+"/tree_directory.hdf5"
    with h5py.File(tree_direc, "r") as td:
        tree_metadata = td[str(treeID)][...]
    return tree_metadata

def get_tree_haloprop(treeID, haloprop):
    """
    Retrieve tree's data for given haloprop from memmapped binary file.

    Parameters
    ----------
    treeID : string

    haloprop : string

    subvolume : string

    Returns
    -------
    tree_haloprop : np.array
        rows of the tree for a particular haloprop.

    """

    dt = dtype.dt[haloprop]
    subvolume = get_subvolume(treeID)
    tree_metadata = get_tree_metadata(treeID)
    tree_length = tree_metadata[LENGTH]
    offset = tree_metadata[OFFSET]
    tree_haloprop = np.memmap(
        filename= 'trees/'+subvolume+'/'+haloprop+'.'+str(dt)+'/'+haloprop+'.data',
        dtype = dt, mode='r',
        shape=(1, tree_length),
        offset = offset * dtype.dt_offset[haloprop]
    )
    return np.array(tree_haloprop[0])

def get_trunk_haloprop(treeID, haloprop):
    """
    Retrieve trunk's data for given haloprop. Slices the trunk from the tree haloprop array.

    Parameters
    ----------
    treeID : string

    haloprop : string

    Returns
    -------
    trunk_haloprop : np.array
        rows of the trunk for a particular haloprop.
    """

    subvolume = get_subvolume(treeID)
    tree_haloprop = get_tree_haloprop(treeID, haloprop)
    tree_depthsort = get_tree_haloprop(treeID, 'haloid_depth_first')
    depthsort_mask = np.argsort(tree_depthsort)

    tree_metadata = get_tree_metadata(treeID)
    last_mainleaf = tree_metadata[HALOID_LAST_MAINLEAF_DEPTHFIRST]
    root = tree_metadata[HALOID_DEPTH_FIRST]
    trunk_len = last_mainleaf - root

    tree_haloprop = tree_haloprop[depthsort_mask] #sort by depth sort mask
    trunk = tree_haloprop[0: (trunk_len+1)] #mainleaf - root = length+1.
    return trunk






