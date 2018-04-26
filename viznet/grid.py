'''
Basic plotlib for neural networks.

feature list:
    1. draw nodes with label.
    2. draw directed/undirected links between two nodes by node labels.
    3. implementation of simple RBM and Feed forward networks.
'''

import numpy as np
import pdb
import numbers
from matplotlib import pyplot as plt
from matplotlib.patches import Circle, Polygon

from .edgenode import Pin
from .brush import EdgeBrush, NodeBrush
from .setting import node_setting

class Grid(object):
    '''
    Args:
        dxy (tuple): space in x, y directions.
        ax: matplotlib.pyplot.Axes.
        num_bit (int): number of bits.
    '''
    line_space = 1.0

    def __init__(self, dxy=(1, 1), ax=None, offset=(0, 0)):
        self.dxy = np.asarray(dxy)
        self.offset = np.asarray(offset)

    def __getitem__(self, ij):
        '''get the position of specific site.'''
        return Pin(self.offset+self.dxy*ij)

    def node_brush(self, *args, **kwargs):
        brush = GridNodeBrush(self, *args, **kwargs)
        return brush

    def block(self, brush, ij1, ij2, pad_x=0.35, pad_y=0.35):
        '''
        strike out a block.

        Args:
            brush (NodeBrush): a brush of style 'box', 'art.rbox' or something rectangular.
            linestart (int): the starting line.
            lineend (int): the ending line > starting line.
            pad_x (float): x padding between gates and box.
            pad_y (float): y padding between gates and box.

        Returns:
            context: context that return boxes.
        '''
        xy = self[ij1]
        xy2 = self[ij2]
        dxy = xy2 - xy
        brush.size = dxy/2. + (pad_x, pad_y)
        b = brush >> (xy + xy2)/2.
        return b

class GridNodeBrush(NodeBrush):
    '''Node Brush defined on a Grid.'''
    def __init__(self, grid, *args, **kwargs):
        self.grid = grid
        self.gridspan = np.array([0, 0])
        super(GridNodeBrush, self).__init__(*args, **kwargs)

    def __rshift__(self, xy):
        return super(GridNodeBrush, self).__rshift__(self.grid[xy])

    def gridwise(self, i, j):
        '''
        resize a node grid-wise

        Args:
            i (int): number of columns.
            j (int): number of rows.

        Return:
            GridNodeBrush: self, as a new brush.
        '''
        color, geo, inner_geo = self._style
        if geo[:9] != 'rectangle' and geo[:9] != 'routangle':
            raise AttributeError('style %s does not support gridwise resize.'%(self.style,))
        ij = np.array([i, j])
        dxy = (ij-self.gridspan)*self.grid.dxy/2./node_setting['basesize']
        self.size = (self._size + dxy)
        self.gridspan = ij
        return self
