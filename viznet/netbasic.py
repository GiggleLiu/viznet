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

__all__ = ['NNPlot', 'DynamicShow',
           'NONE', 'YELLOW', 'GREEN', 'RED', 'BLUE', 'VIOLET', 'NODE_THEME_DICT']

NONE = 'none'
YELLOW = '#FFFF77'
GREEN = '#55CC77'
RED = '#FF6644'
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
    def __init__(self, ax, fontsize=12):
        self.ax = ax
        self.node_dict = {}
        self.edge_dict = {}
        self.fontsize = fontsize

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
                            head_length=0.12 if directed else 0, width=0.015,
                            head_width=8e-2, fc='#333333',# ec='#333333',
                            length_includes_head=True, lw=0, edgecolor='none')

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
            self.ax.text(xy[0], xy[1], name, va='center', ha='center', fontsize=self.fontsize)
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

    def text_node(self, name, text, offset=(0,0)):
        '''
        add texts for a sequence of nodes.
        '''
        c = self.node_dict[name]
        x, y = c.center + np.array(offset)
        self.ax.text(x, y, text, va='center', ha='center', fontsize=self.fontsize)

    def add_node_sequence(self, num_node, token, y, kind='basic', radius=0.2, offset=(0, 0), show_name=True):
        '''
        add a sequence of nodes along x-direction.
        '''
        x_list = np.arange(-num_node / 2. + 0.5, num_node / 2., 1)
        for i, xy in enumerate(zip(x_list + offset[0], y * np.ones(num_node) + offset[1])):
            self.add_node(self.auto_name(token, i), xy, kind=kind,
                          radius=radius, show_name=show_name)

    def connect_layers(self, start_token, end_token, one2one=False, directed=False):
        i = 0
        while(self.auto_name(start_token, i) in self.node_dict):
            if one2one:
                self.connect(self.auto_name(start_token, i),
                             self.auto_name(end_token, i), directed=directed)
            else:
                j = 0
                while(self.auto_name(end_token, j) in self.node_dict):
                    self.connect(self.auto_name(start_token, i),
                                 self.auto_name(end_token, j), directed=directed)
                    j += 1
            i += 1

    def text_node_sequence(self, token, text_list, offset=(0,0)):
        '''
        add texts for a sequence of nodes.
        '''
        for i, t in enumerate(text_list):
            c = self.text_node(self.auto_name(token, i), t, offset)

    def auto_name(self, token, i):
        return r'$%s_%d$' % (token, i + 1)


class DynamicShow():
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
        with DynamicShow() as ds:
            c = Circle([2, 2], radius=1.0)
            ds.ax.add_patch(c)
    '''

    def __init__(self, figsize=(6, 4), filename=None, dpi=300):
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
        plt.tight_layout()
        if self.filename is not None:
            print('Press `c` to save figure to "%s", `Ctrl+d` to break >>'%self.filename)
            pdb.set_trace()
            plt.savefig(self.filename, dpi=300)
        else:
            pdb.set_trace()
