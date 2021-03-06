from build import subvolume_directory, tree_directory, haloprop_binary


def build(subvolume):
    """
    Converts subvolume ascii file into accesible data via tree ID.

    1) Adds all tree ID's in the subvolume to the subvolume directory. 

    2) Build binary files for subvolume halo properties.
    properties added: mvir, haloid_next_coprog_depthfirst, haloid_depth_first, upid, scale

    3) Adds tree metadata for each tree in the subvolume to tree directory.
    tree metadata: length, offset, depthfirst ID, lastmainleaf ID of each tree
    
    Parameters
    ----------
    subvolume : string
        Name of subvolume

    Examples
    --------
    
    >>> build('0_0_0')
    
    """
    
    tree_directory.create(subvolume)
    haloprops = ['mvir', 'haloid_next_coprog_depthfirst', 'haloid_depth_first', 'upid', 'scale']
    for p in haloprops:
        haloprop_binary.create(subvolume, p)
    subvolume_directory.create(subvolume)

