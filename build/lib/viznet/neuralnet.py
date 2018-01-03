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

__all__ = ['NNPlot', 'DynamicShow',
class NNPlot(object):
    '''
    Args:
        line_lw (bool, default=1): line width.
        line_color (bool, default='#333333'): line default color of lines.
        distance (tuple, default=(1,0)): space between two nodes.
    '''
    def __init__(self, ax, fontsize=12, line_lw=1, line_color='#333333', distance=(1, 0)):
        self.ax= ax
        self.node_dict= {}
        self.edge_dict= {}
        self.fontsize= fontsize
        self.line_lw= line_lw
        self.line_color= line_color
        self.distance= distance

    def add_node_sequence(self, num_node, token, offset, kind='basic', radius=0.2,
            show_name=True):
        '''
        add a sequence of nodes along x-direction.

        Args:
            num_node (int): number of node to be added.
            token (int): the token to name this serie of nodes. e.g. token 'x' will generate node serie `$x_1$, $x_2$ ...`.
            offset (tuple|float): offset in x-y directions. if a number is passed, offset along perpendicular direction with respect to :data:`self.distance`.
            kind (str, default='basic'): the kind of node, see `NODE_THEME_DICT` for reference.
            radius (float, default=0.2): the size of ball.
            show_name (str|bool, default=True): display the name of each node, if str provided, display string.

        Return:
            list: a list of node names, you can visit this node by accesing `self.node_dict[node_name]`.
        '''
        x_list= np.arange(-num_node / 2. + 0.5, num_node / 2., 1)
        xylist = np.asarray(self.distance) * x_list[:, None]
        return self._add_node_sequence(xylist, token, offset, kind, radius, show_name)

    def _add_node_sequence(self, xylist, token, offset, kind, radius, show_name):
        '''
        add a sequence of nodes along x-direction.

        Args:
            token (int): the token to name this serie of nodes. e.g. token 'x' will generate node serie `$x_1$, $x_2$ ...`.
            offset (tuple|float): offset in x-y directions. if a number is passed, offset along perpendicular direction with respect to :data:`self.distance`.
            kind (str, default='basic'): the kind of node, see `NODE_THEME_DICT` for reference.
            radius (float, default=0.2): the size of ball.
            show_name (str|bool, default=True): display the name of each node, if str provided, display string.

        Return:
            list: a list of node names, you can visit this node by accesing `self.node_dict[node_name]`.
        '''
        if isinstance(offset, numbers.Number):
            offset= np.array([-self.distance[1], self.distance[0]]) * offset
        node_name_list= []
        for i, xy in enumerate(zip(xylist[:, 0] + offset[0], xylist[:, 1] + offset[1])):
            node_name= self.auto_name(token, i)
            self.add_node(node_name, xy, kind=kind,
                          radius=radius, show_name=show_name)
            node_name_list.append(node_name)
        return node_name_list


    def connect_layers(self, start_token, end_token, one2one=False,
            directed=False):
        '''
        Args:
            start_token (str): the start layer generation token (pointed from).
            end_token (str): the end layer generation token (pointed to).
            one2one (bool, default=False): one to one connected if True else all to all.
            directed (bool, default=False): arrows are directed if True.
        '''
        i= 0
        while(self.auto_name(start_token, i) in self.node_dict):
            if one2one:
                self.connect(self.auto_name(start_token, i),
                             self.auto_name(end_token, i), directed=directed)
            else:
                j= 0
                while(self.auto_name(end_token, j) in self.node_dict):
                    self.connect(self.auto_name(start_token, i),
                                 self.auto_name(end_token, j), directed=directed)
                    j += 1
            i += 1

    def text_node_sequence(self, token, text_list, offset=(0, 0)):
        '''
        add texts for a sequence of nodes.

        Args:
            token (str): the layer generation token.
            text_list (list): a list of text.
            offset (tuple, default=(0,0)): offset in x-y directions.
        '''
        for i, t in enumerate(text_list):
            self.text_node(self.auto_name(token, i), t, offset)

    def auto_name(self, token, i):
        '''
        auto-naming system

        Args:
            token (str): layer generation token.
            i (int): the id of node in a layer, from 1 to N.

        Return:
            str: the name of node.
        '''
        return r'$%s_%d$' % (token, i + 1)

    def context(self, attr, val):
        '''
        change attribute in this context.

        Args:
            attr (str): the attribute to be changed.
            val (obj): the target value that used in this context.

        Return:
            obj: Context object.
        '''
        oval= getattr(self, attr)
        class Brush():
            def __enter__(brush):
                setattr(self, attr, val)
            def __exit__(brush, *args):
                setattr(self, attr, oval)
        return Brush()
