import h5py

def header_len(fname):
    """ 
    Get number of header lines.

    """

    h = 0
    for i, line in enumerate(open(fname)):
        if(line[0] == '#'):
            h += 1
        else:
            return h
    return


def create(subvolume):
    """
    Adds all treeID's in the subvolume to the subvolume directory (hdf5 file). 

    User can retrieve data like:

    subvolume_directory['treeID'] --> 'subvolume'

    Parameters
    ----------
    subvolume : string

    Examples
    --------

    >>> create('0_0_0')
    >>> #now you can retrieve the subvolume from subvolume_directory.hdf5
    >>> treeID = '3060286872'
    >>> with h5py.File('subvolume_directory.hdf5', 'r') as subvolume_directory:
    >>>     subvolume = subvolume_directory[treeID][...][0]
    >>> print subvolume
    >>> '0_0_0'
    
    """
    subvolume_file = 'tree_ascii_data/tree_' + subvolume + '.dat'
    subvolume_directory = 'subvolume_directory.hdf5'
    print 'adding to subvolume directory at', subvolume_directory
    h = header_len(subvolume_file)
    with open(subvolume_file) as f:
        for _ in xrange(0, h):
                f.readline()
        num_trees = int(f.readline())
        n = 0
        with h5py.File(subvolume_directory,"w") as hf: 
            for line in f:
                if(line[0] == '#'):
                    tree_id = line[6:].strip('\n')
                    print '#tree', str(tree_id) + '/' + str(num_trees)
                    hf[tree_id] = [subvolume]
                    n += 1

    return 


