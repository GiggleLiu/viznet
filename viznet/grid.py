'''
Basic plotlib for neural networks.

feature list:
    1. draw nodes with label.
    2. draw directed/undirected links between two nodes by node labels.
    3. implementation of simple RBM and Feed forward networks.
'''

import numpy as np

__all__ = ['Grid']

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
        self.dxy = np.asarray(dxy)
        self.offset = np.asarray(offset)

    def __getitem__(self, ij):
        '''get the pin of specific site.'''
        i, j = ij
        if isinstance(i, slice):
            if i.start is None or j.start is None:
                raise ValueError('slice not valid!')
            dx, dy = self.dxy
            ox, oy = self.offset
            istart, jstart = self[i.start, j.start]
            istop, jstop = self[i.stop, j.stop]
            return slice(istart, istop), slice(jstart, jstop)
        else:
            return self.offset+self.dxy*ij
