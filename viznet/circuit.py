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

    def __init__(self, ax, num_bit, x=0,  **kwargs):
        self.x = x
        self.node_dict = dict(
            zip(range(num_bit), [[Pin((self.x, -i))] for i in range(num_bit)]))
        self.edge = EdgeBrush('---', ax, **kwargs)

    def gate(self, brush, position, text=None, fontsize=18):
        '''
        place a gate at specific position.
        '''
        if not hasattr(brush, '__iter__'):
            brush = (brush,)
            return_list = False
        else:
            return_list = True
        if not hasattr(position, '__iter__'):
            position = (position,)
        if len(brush) == 1 and len(position) > 1:
            position_node = (np.mean(position),)
        elif len(brush) > 1 and len(position) > 1 and len(brush) != len(position):
            raise ValueError()
        else:
            position_node = position

        node_list = []
        for b, y in zip(brush, position_node):
            node = b >> (self.x, -y)

            # connect nodes
            if len(node_list) >= 1:
                self.edge >> (node_list[-1], node)
            if position_node is position:
                self.edge >> (self.node_dict[y][-1], node)
                self.node_dict[y].append(node)
            else:
                for y in position:
                    prenode = self.node_dict[y][-1]
                    lnode = node.pin('left', align=prenode)
                    rnode = node.pin('right', align=prenode)
                    self.node_dict[y].append(lnode)
                    self.node_dict[y].append(rnode)
                    self.edge >> (prenode, lnode)
            node_list.append(node)

        if text is not None:
            node.text(text, fontsize=fontsize)
        return node_list if return_list else node_list[0]
