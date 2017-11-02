'''
Basic plotlib for neural networks.

feature list:
    1. draw nodes with label.
    2. draw directed/undirected links between two nodes by node labels.
    3. implementation of simple RBM and Feed forward networks.
'''

from __future__ import division

import numpy as np
import pdb
from matplotlib import pyplot as plt
from matplotlib.patches import Circle, Polygon

__all__ = ['NNPlot', 'draw_rbm', 'draw_feed_forward', 'DynamicPlot',
           'NONE', 'YELLOW', 'GREEN', 'RED', 'BLUE', 'VIOLET', 'NODE_THEME_DICT']

NONE = 'none'
YELLOW = '#FFFF77'
GREEN = '#55CC77'
RED = '#DD3377'
BLUE = '#3399DD'
VIOLET = '#DD99DD'

NODE_THEME_DICT = {
    'basic': (NONE, 'none'),
    'backfed': (YELLOW, 'circle'),
    'input': (YELLOW, 'none'),
    'noisy_input': (YELLOW, 'triangle'),
    'hidden': (GREEN, 'none'),
    'probablistic_hidden': (GREEN, 'circle'),
    'spiking_hidden': (GREEN, 'triangle'),
    'output': (RED, 'none'),
    'match_input_output': (RED, 'circle'),
    'recurrent': (BLUE, 'none'),
    'memory': (BLUE, 'circle'),
    'different_memory': (BLUE, 'triangle'),
    'kernel': (VIOLET, 'none'),
    'convolution': (VIOLET, 'circle'),
    'pooling': (VIOLET, 'circle'),
}


class NNPlot(object):
    def __init__(self, ax):
        self.ax = ax
        self.node_dict = {}
        self.edge_dict = {}

    def connect(self, start, end, directed=False):
        '''connect start node and end node'''
        sn = self.node_dict[start]
        en = self.node_dict[end]
        sxy, exy = np.array(sn.center), np.array(en.center)
        d = exy - sxy
        unit_d = d / np.linalg.norm(d)
        sxy = unit_d * sn.radius + sxy
        exy = -unit_d * en.radius + exy
        d = exy - sxy
        arr = self.ax.arrow(sxy[0], sxy[1], d[0], d[1],
                            head_length=8e-2 if directed else 0,
                            head_width=5e-2, fc='#333333', ec='#333333',
                            length_includes_head=True, lw=1)

        self.edge_dict['%s-%s' % (start, end)] = arr

    def add_node(self, name, xy, radius=0.2, kind='basic', show_name=True):
        '''
        add a node

        Args:
            kind (str|tuple): 
                * if it is a string, search NODE_THEME_DICT for a configuration.
                * if it is a tuple, it should be a (color, geometry) pair.
        '''
        if isinstance(kind, str):
            kind = NODE_THEME_DICT[kind]
        color, geo = kind

        c = Circle(xy, radius, edgecolor='k',
                   facecolor=color, lw=0.7, zorder=0)
        if show_name:
            self.ax.text(xy[0], xy[1], name, va='center', ha='center')
        self.ax.add_patch(c)

        # add a geometric patch at the top of circle.
        if geo != 'none':
            if geo == 'circle':
                g = Circle(xy, 0.7 * radius, edgecolor='k',
                           facecolor='none', lw=0.7, zorder=101)
            elif geo == 'triangle':
                g = Polygon(xy=np.array([[-0.5 * np.sqrt(3), -0.5], [0.5 * np.sqrt(3), -0.5], [
                            0, 1]]) * 0.7 * radius + xy, edgecolor='k', facecolor='none', lw=0.7, zorder=101)
            else:
                raise ValueError('Geometry %s is not allowed!' % geo)
            self.ax.add_patch(g)

        # for BLUE nodes, add a self-loop (Stands for Recurrent Unit)
        if color == BLUE:
            loop = Circle((xy[0], xy[1] + 1.2 * radius), 0.5 * radius,
                          edgecolor='k', facecolor='none', lw=0.7, zorder=-5)
            self.ax.add_patch(loop)

        self.node_dict[name] = c

    def add_node_sequence(self, num_node, token, y, kind='basic', radius=0.2, offset=(0, 0), show_name=True):
        '''
        add a sequence of nodes along x-direction.
        '''
        x_list = np.arange(-num_node / 2. + 0.5, num_node / 2., 1)
        for i, xy in enumerate(zip(x_list + offset[0], y * np.ones(num_node) + offset[1])):
            self.add_node(self.auto_name(token, i), xy, kind=kind,
                          radius=radius, show_name=show_name)

    def connect_layers(self, start_token, end_token, directed=False):
        i = 0
        while(self.auto_name(start_token, i) in self.node_dict):
            j = 0
            while(self.auto_name(end_token, j) in self.node_dict):
                self.connect(self.auto_name(start_token, i),
                             self.auto_name(end_token, j), directed=directed)
                j += 1
            i += 1

    def auto_name(self, token, i):
        return r'$%s_%d$' % (token, i + 1)


def draw_rbm(ax, num_node_visible, num_node_hidden):
    '''
    draw a restricted boltzmann machine.

    Args:
        num_node_visible (int), number of visible nodes.
        num_node_hidden (int), number of hidden nodes.
    '''
    handler = NNPlot(ax)
    # visible layers
    handler.add_node_sequence(
        num_node_visible, '\sigma^z', 0, kind='input', radius=0.3)

    # hidden layers
    handler.add_node_sequence(num_node_hidden, 'h',
                              1.5, kind='hidden', radius=0.2)

    # connect them
    handler.connect_layers('\sigma^z', 'h', False)


def draw_feed_forward(ax, num_node_list):
    '''
    draw a feed forward neural network.

    Args:
        num_node_list (list<int>): number of nodes in each layer.
    '''
    handler = NNPlot(ax)
    num_hidden_layer = len(num_node_list) - 2
    token_list = ['\sigma^z'] + \
        ['y^{(i)}' for num_node_list in num_node_list[1:-1]] + ['\psi']
    kind_list = ['input'] + ['hidden'] * num_hidden_layer + ['output']
    radius_list = [0.3] + [0.2] * num_hidden_layer + [0.3]
    y_list = 1.5 * np.arange(len(num_node_list))

    for n, token, kind, radius, y in zip(num_node_list, token_list, kind_list, radius_list, y_list):
        handler.add_node_sequence(n, token, y, kind=kind, radius=radius)

    for st, et in zip(token_list[:-1], token_list[1:]):
        handler.connect_layers(st, et, directed=True)


class DynamicPlot():
    '''
    Dynamic plot context, intended for displaying geometries.
    like removing axes, equal axis, dynamically tune your figure and save it.

    Args:
        figsize (tuple, default=(6,4)): figure size.
        filename (filename, str): filename to store generated figure, if None, it will not save a figure.

    Attributes:
        figsize (tuple, default=(6,4)): figure size.
        filename (filename, str): filename to store generated figure, if None, it will not save a figure.
        ax (Axes): matplotlib Axes instance.

    Examples:
        with DynamicPlot() as dp:
            c = Circle([2, 2], radius=1.0)
            dp.ax.add_patch(c)
    '''

    def __init__(self, figsize=(6, 4), filename=None):
        self.figsize = figsize
        self.filename = filename
        self.ax = None

    def __enter__(self):
        plt.ion()
        plt.figure(figsize=self.figsize)
        self.ax = plt.gca()
        return self

    def __exit__(self, *args):
        plt.axis('equal')
        plt.axis('off')
        if self.filename is not None:
            print('Press `C` to save figure, `Ctrl+D` to break >>')
            pdb.set_trace()
            plt.savefig(self.filename)
        else:
            pdb.set_trace()
