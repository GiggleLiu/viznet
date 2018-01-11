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
from .brush import EdgeBrush

__all__ = ['QuantumCircuit']


class QuantumCircuit(object):
    '''
    Args:
        ax: matplotlib.pyplot.Axes.
        num_bit (int): number of bits.
    '''

    def __init__(self, ax, num_bit):
        self.x = 0
        self.node_dict = dict(zip(range(num_bit), [[Pin((0,i))] for i in range(num_bit)]))
        self.edge = EdgeBrush('---', ax)

    def gate(self, brush, position, text=None):
        '''
        place a gate at specific position.
        '''
        if not isinstance(brush, tuple):
            brush = (brush,)
        if not isinstance(position, tuple):
            position = (position,)
        if len(brush) == 1 and len(position)>1:
            position_node = (np.mean(position),)
        elif len(brush)>1 and len(position)>1 and len(brush)!=len(position):
            raise ValueError()
        else:
            position_node = position

        node_pre = None
        for b, y in zip(brush, position_node):
            node = b >> (self.x, y)

            # connect nodes
            if node_pre is not None:
                self.edge >> (node_pre, node)
            if position_node is position:
                self.edge >> (self.node_dict[y][-1], node)
                self.node_dict[y].append(node)
                node_pre = node
            else:
                for y in position:
                    prenode = self.node_dict[y][-1]
                    lnode = node.pin('left', align=prenode)
                    rnode = node.pin('right', align=prenode)
                    self.node_dict[y].append(lnode)
                    self.node_dict[y].append(rnode)
                    self.edge >> (prenode, lnode)

        if text is not None:
            node.text(text, fontsize=18)
