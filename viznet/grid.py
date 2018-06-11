'''
Basic plotlib for neural networks.

feature list:
    1. draw nodes with label.
    2. draw directed/undirected links between two nodes by node labels.
    3. implementation of simple RBM and Feed forward networks.
'''

import numpy as np

def _v(dxy):
    if np.shape(dxy) == (2,):  # rectangle region
        return np.array([[dxy[0], 0], [0, dxy[1]]])
    return np.asarray(dxy)

class Grid(object):
    '''
    Grid for affine transformation.

    Args:
        dxy (tuple): space in x, y directions.
        ax: matplotlib.pyplot.Axes.
        offset (tuple): the global offset.
    '''
    line_space = 1.0

    def __init__(self, dxy=(1, 1), ax=None, offset=(0, 0)):
        vxy = _v(dxy)
        if not (vxy.ndim == 2 and vxy.shape[1]==2 and 2 == len(offset)):
            raise Exception("Dimension mismatch!")
        self.dxy = np.asarray(dxy)
        self.offset = np.asarray(offset)

    @property
    def ndim(self):
        return length(self.dxy)

    def __getitem__(self, ij):
        '''get the pin of specific site.'''
        if isinstance(ij[0], slice):
            if np.ndim(self.dxy) == 1:  # rectangular
                i, j = ij
                if i.start is None or j.start is None:
                    raise ValueError('slice not valid!')
                dx, dy = self.dxy
                istart, jstart = self[i.start, j.start]
                istop, jstop = self[i.stop, j.stop]
                return slice(istart, istop), slice(jstart, jstop)
            else:
                raise NotImplementedError("Grid Region for non-rectangular regions will be supported in the future.")
        else:
            return self.offset + (_v(self.dxy)*np.array(ij)[:,None]).sum(axis=0)
