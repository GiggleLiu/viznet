'''
Basic plotlib for neural networks.

feature list:
    1. draw nodes with label.
    2. draw directed/undirected links between two nodes by node labels.
    3. implementation of simple RBM and Feed forward networks.
'''

import numpy as np
from matplotlib import pyplot as plt
from matplotlib.patches import Circle

__all__ = ['NNPlot', 'draw_rbm', 'draw_feed_forward']

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

    def add_node(self, name, xy, color, radius=0.2):
        '''add a node'''
        c = plt.Circle(xy, radius, edgecolor='k', facecolor=color, lw=0.7)
        self.ax.text(xy[0], xy[1], name, va='center', ha='center')
        self.ax.add_patch(c)

        self.node_dict[name] = c

    def add_node_sequence(self, num_node, token, y, color, radius=0.2, offset=(0,0)):
        '''
        add a sequence of nodes along x-direction.
        '''
        x_list = np.arange(-num_node / 2. + 0.5, num_node / 2., 1)
        for i, xy in enumerate(zip(x_list+offset[0], y * np.ones(num_node)+offset[1])):
            self.add_node(self.auto_name(token, i), xy, color, radius=radius)

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
    handler.add_node_sequence(num_node_visible, '\sigma^z', 0, color='#DDDD55', radius=0.3)

    # hidden layers
    handler.add_node_sequence(num_node_hidden, 'h', 1.5, color='#888888', radius=0.2)

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
    token_list = ['\sigma^z'] + ['y^{(i)}' for num_node_list in num_node_list[1:-1]] + ['\psi']
    color_list = ['#DDDD55'] + ['#888888'] * num_hidden_layer + ['#77DDAA']
    radius_list = [0.3] + [0.2] * num_hidden_layer + [0.3]
    y_list = 1.5 * np.arange(len(num_node_list))

    for n, token, color, radius, y in zip(num_node_list, token_list, color_list, radius_list, y_list):
        handler.add_node_sequence(n, token, y, color, radius=radius)

    for st, et in zip(token_list[:-1], token_list[1:]):
        handler.connect_layers(st, et, directed=True)

