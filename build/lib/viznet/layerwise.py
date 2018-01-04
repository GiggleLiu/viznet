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

__all__ = ['Layerwise']


class Layerwise(object):
    '''
    Args:
        line_lw (bool, default=1): line width.
        line_color (bool, default='#333333'): line default color of lines.
        distance (tuple, default=(1,0)): space between two nodes.
    '''

    def __init__(self, distance=(1, 0)):
        self.node_dict = {}
        self.edge_dict = {}
        self.distance = distance

    def node_sequence(self, token, num_node, brush, offset):
        '''
        add a sequence of nodes along x-direction.

        Args:
            num_node (int): number of node to be added.
            token (int): the token to name this serie of nodes. e.g. token 'x' will generate node serie `$x_1$, $x_2$ ...`.
            offset (tuple|float): offset in x-y directions. if a number is passed, offset along perpendicular direction with respect to :data:`self.distance`.
            brush (NodeBrush): brush instance.

        Return:
            list: a list of node names, you can visit this node by accesing `self.node_dict[node_name]`.
        '''
        x_list = np.arange(-num_node / 2. + 0.5, num_node / 2., 1)
        xylist = np.asarray(self.distance) * x_list[:, None]
        if isinstance(offset, numbers.Number):
            offset = np.array([-self.distance[1], self.distance[0]]) * offset

        node_list = []
        for i, xy in enumerate(zip(xylist[:, 0] + offset[0], xylist[:, 1] + offset[1])):
            node_list.append(brush >> xy)
        self.node_dict[token] = node_list
        return node_list

    def connect121(self, start_token, end_token, brush):
        '''
        Args:
            start_token (str): the start layer generation token (pointed from).
            end_token (str): the end layer generation token (pointed to).
            brush (EdgeBrush): edge brush instance.
        '''
        return self._connect(start_token, end_token, brush, one2one=True)

    def connecta2a(self, start_token, end_token, brush):
        '''
        Args:
            start_token (str): the start layer generation token (pointed from).
            end_token (str): the end layer generation token (pointed to).
            brush (EdgeBrush): edge brush instance.
        '''
        return self._connect(start_token, end_token, brush, one2one=False)

    def _connect(self, start_token, end_token, brush, one2one=False):
        end_nodes = self.node_dict[end_token]
        edge_list = []
        for i, start_node in enumerate(self.node_dict[start_token]):
            if one2one:
                edge_list.append(brush >> (start_node, end_nodes[i]))
            else:
                for end_node in end_nodes:
                    edge_list.append(brush >> (start_node, end_node))
        self.edge_dict[start_token + '-' + end_token] = edge_list
        return edge_list

    def text(self, token, text_list=None, position='center', text_offset=None, color='k', fontsize=None):
        '''
        add texts for a sequence of nodes.

        Args:
            token (str): the layer generation token.
            text_list (list): a list of text.
            position (str): position of texts.
        '''
        node_list = self.node_dict[token]
        if text_list is None:
            # use auto name
            text_list = [self.autoname(token, i) for i in range(len(node_list))]
        for node, text in zip(node_list, text_list):
            node.text(text, position=position,
                      text_offset=text_offset, color=color, fontsize=fontsize)

    def autoname(self, token, i):
        '''
        auto-naming system

        Args:
            token (str): layer generation token.
            i (int): the id of node in a layer, from 1 to N.

        Return:
            str: the name of node.
        '''
        return r'$%s_%d$' % (token, i + 1)
