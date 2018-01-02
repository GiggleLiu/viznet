'''
Plots for zoo of nets.
'''

import numpy as np

from .neuralnet import NNPlot

__all__ = ['draw_rbm', 'draw_feed_forward']

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
        ['y^{(%s)}'%(i+1) for i in range(num_hidden_layer)] + ['\psi']
    kind_list = ['input'] + ['hidden'] * num_hidden_layer + ['output']
    radius_list = [0.3] + [0.2] * num_hidden_layer + [0.3]
    y_list = 1.5 * np.arange(len(num_node_list))

    for n, token, kind, radius, y in zip(num_node_list, token_list, kind_list, radius_list, y_list):
        handler.add_node_sequence(n, token, y, kind=kind, radius=radius)

    for st, et in zip(token_list[:-1], token_list[1:]):
        handler.connect_layers(st, et, directed=True)
