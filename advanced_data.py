import os
import numpy as np
import h5py
import matplotlib.pyplot as plt
from dtype import dt, dt_offset


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

    with h5py.File('subvolume_directory.hdf5', "r") as svd:
        subvolume = svd[str(treeID)][...][0]
    return subvolume

def get_tree_metadata(treeID, subvolume):
    """
    Retrieve tree's metadata.

    Parameters
    ----------
    treeID : string
    
    """

    tree_direc = "trees/"+subvolume+"/tree_directory.hdf5"
    with h5py.File(tree_direc, "r") as td:
        tree_metadata = td[str(treeID)][...]     
    return tree_metadata

def get_tree_haloprop(treeID, haloprop, subvolume):
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

    dtype = dt[haloprop]
    tree_metadata = get_tree_metadata(treeID, subvolume)
    tree_length = tree_metadata[LENGTH]
    offset = tree_metadata[OFFSET]   
    tree_haloprop = np.memmap(
        filename= 'trees/'+subvolume+'/'+haloprop+'.'+str(dtype)+'/'+haloprop+'.data', 
        dtype = dtype, mode='r', 
        shape=(1, tree_length), 
        offset = offset * dt_offset[haloprop]
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
    tree_haloprop = get_tree_haloprop(treeID, haloprop, subvolume)
    tree_depthsort = get_tree_haloprop(treeID, 'haloid_depth_first', subvolume)
    depthsort_mask = np.argsort(tree_depthsort)
    
    tree_metadata = get_tree_metadata(treeID, subvolume)
    last_mainleaf = tree_metadata[HALOID_LAST_MAINLEAF_DEPTHFIRST]
    root = tree_metadata[HALOID_DEPTH_FIRST]
    trunk_len = last_mainleaf - root

    tree_haloprop = tree_haloprop[depthsort_mask] #sort by depth sort mask
    trunk = tree_haloprop[0: (trunk_len+1)] #mainleaf - root = length+1.
    return trunk

def clumpy_accretion(treeID):
    """
    Retrieve the clumpy accretion history for the trunk of a treeID.

    Parameters
    ----------
    treeID : string

    Returns
    -------
    clumpy_accretion : np.array
        rows of trunk for its clumpy accretion history.
    """

    subvolume = get_subvolume(treeID)
    tree_metadata = get_tree_metadata(treeID, subvolume)
    tree_mvir = get_tree_haloprop(treeID, 'mvir', subvolume)
    tree_depthsort = get_tree_haloprop(treeID, 'haloid_depth_first', subvolume)
    depthsort_mask = np.argsort(tree_depthsort)
    tree_mvir_sorted = tree_mvir[depthsort_mask] #sort by depthsort ID
    tree_coprog = get_tree_haloprop(treeID, 'haloid_next_coprog_depthfirst', subvolume)
    tree_coprog_sorted = tree_coprog[depthsort_mask]

    trunk_coprog = get_trunk_haloprop(treeID, 'haloid_next_coprog_depthfirst')
    trunk_len = len(trunk_coprog)

    clumpy_history = [0] * (trunk_len - 1)
    trunk_depth = get_trunk_haloprop(treeID, 'haloid_depth_first')
    root = tree_metadata[HALOID_DEPTH_FIRST]

    for i in range(0, trunk_len - 1): #last trunk leaf has no progenitors
        clumpy = 0
        coprogenitor = trunk_coprog[i + 1]
        while(coprogenitor != -1.0):
            coprog_index = coprogenitor - root
            clumpy += tree_mvir_sorted[coprog_index]
            coprogenitor = tree_coprog_sorted[coprog_index]
        clumpy_history[i] = clumpy

    return np.array(clumpy_history)

def smooth_accretion(treeID):
    """
    Retrieve the smooth accretion history for the trunk of a treeID.
    smooth[i] = (mass[i] - mass[i+1]) - clumpy[i]

    Parameters
    ----------
    treeID : string

    Returns
    -------
    smooth_accretion : np.array
        rows of trunk for its smooth accretion history.
    """

    trunk_mass = get_trunk_haloprop(treeID, 'mvir')
    smooth_history = []
    clumpy_history = clumpy_accretion(treeID)
    for i in range(0, len(trunk_mass) - 1):
        smooth = trunk_mass[i] - clumpy_history[i] - trunk_mass[i + 1]
        smooth_history.append(smooth)
    return np.array(smooth_history)

def plot_accretion(treeID):
    """
    Plots clumpy, smooth, total mass, and clumpy + smooth accretion
    total mass should equal clumpy + smooth

    Parameters
    ----------
    treeID : string

    """

    clumpy_history = clumpy_accretion(treeID)
    smooth_history = smooth_accretion(treeID)
    mass_history = get_trunk_haloprop(treeID, 'mvir')
    mass_history = mass_history[:len(mass_history)-1]

    clumpy_plus_smooth = [0] * len(clumpy_history)
    for i, val in enumerate(clumpy_history):
        clumpy_plus_smooth[i] = clumpy_history[i] + smooth_history[i]

    x1 = np.linspace(1, 0, len(smooth_history))
    clumpy, = plt.plot(x1, clumpy_history, label='clumpy', lw=2)
    smooth, = plt.plot(x1, smooth_history, label='smooth', lw=2)
    total, = plt.plot(x1, mass_history, label='total mass', lw= 2)
    clumpy_plus_smooth, = plt.plot(x1, mass_history, label='clumpy + smooth')
    plt.legend(handles=[clumpy, smooth, total, clumpy_plus_smooth])
    plt.title('Mass Accretion over Time')
    plt.show()

def clumpiness(treeID):
    """
    Returns clumpy statistic for a given treeID. 

    clumpiness = (change in mass due to clumpy accretion)/(change in total mass)

    The timeframe is set to between current day and z = 1.

    Parameters
    ----------
    treeID : string

    Returns
    -------
    clumpiness : float
        summary statistic of the clumpiness of a tree's mass accretion history.

    Examples
    --------

    >>> c = clumpiness('3060299107')
    >>> print c
    >>> 'clumpiness:  0.0974984867952'

    """

    trunk_scale = get_trunk_haloprop(treeID, 'scale')
    index = 0
    for i, s in enumerate(trunk_scale):
        if(s < .5): #redshift = 1
            index = i
            break
    trunk_mass = get_trunk_haloprop(treeID, 'mvir')
    mass_delta = trunk_mass[0] - trunk_mass[index]
    # print 'mass delta', mass_delta
    trunk_clumpy = clumpy_accretion(treeID)

    clumpy_delta = 0
    for i in xrange(0, index+1):
        clumpy_delta += trunk_clumpy[i]

    # print 'clumpy delta', clumpy_delta
    fraction_clumpy = clumpy_delta/mass_delta
    print 'clumpiness: ', fraction_clumpy

    return fraction_clumpy

def smoothness(treeID):
    """
    Returns smooth statistic for a given treeID. 

    smothness = (change in mass due to smooth accretion)/(change in total mass)

    The timeframe is set to between current day and z = 1.

    Parameters
    ----------
    treeID : string

    Returns
    -------
    smoothness : float
        summary statistic of the smoothness of a tree's mass accretion history.

    """

    trunk_scale = get_trunk_haloprop(treeID, 'scale')
    index = 0
    for i, s in enumerate(trunk_scale):
        if(s < .5): #start at redshift 1
            index = i
            break

    trunk_mass = get_trunk_haloprop(treeID, 'mvir')
    trunk_smooth = smooth_accretion(treeID)

    mass_delta = trunk_mass[0] - trunk_mass[index]
    # print mass_delta
    smooth_delta = 0
    # mass_delta_2 = 0

    for i in xrange(0, index + 1):
        j = index - i
        # print trunk_mass[j] - trunk_smooth[j]
        # print '\n'
        # mass_delta_2 += trunk_mass[j]
        smooth_delta += trunk_smooth[j]

    # print mass_delta - smooth_delta
    print 'smooth delta', smooth_delta
    fraction_smooth = smooth_delta/mass_delta
    print 'fraction smooth', fraction_smooth
    return fraction_smooth

def is_host_halo(treeID):
    trunk_upid = get_trunk_haloprop(treeID, 'upid')
    for i, val in enumerate(trunk_upid):
        if(val != -1):
            subhaloID = trunk_upid[i]
            break
    print subhaloID