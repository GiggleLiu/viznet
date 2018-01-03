'''
Plots for zoo of nets.
'''

import numpy as np

from .layerwise import Layerwise
from .brush import NodeBrush, EdgeBrush

__all__ = ['draw_rbm', 'draw_feed_forward']


def draw_rbm(ax, num_node_visible, num_node_hidden):
    '''
    draw a restricted boltzmann machine.

    Args:
        num_node_visible (int), number of visible nodes.
        num_node_hidden (int), number of hidden nodes.
    '''
    handler = Layerwise()
    # visible layers
    nb1 = NodeBrush('nn.backfed', ax)
    nb2 = NodeBrush('nn.probablistic_hidden', ax)
    eb = EdgeBrush('undirected', ax)

    handler.add_node_sequence(
        '\sigma^z', num_node_visible, offset=0, brush=nb1)

    # hidden layers
    handler.add_node_sequence('h', num_node_hidden, offset=1, brush=nb2)

    # connect them
    handler.connecta2a('\sigma^z', 'h', eb)


def draw_feed_forward(ax, num_node_list):
    '''
    draw a feed forward neural network.

    Args:
        num_node_list (list<int>): number of nodes in each layer.
    '''
    handler = Layerwise()
    num_hidden_layer = len(num_node_list) - 2
    token_list = ['\sigma^z'] + \
        ['y^{(%s)}' % (i + 1) for i in range(num_hidden_layer)] + ['\psi']
    kind_list = ['nn.input'] + ['nn.hidden'] * num_hidden_layer + ['nn.output']
    radius_list = [0.3] + [0.2] * num_hidden_layer + [0.3]
    y_list = 1.5 * np.arange(len(num_node_list))

    for n, token, kind, radius, y in zip(num_node_list, token_list, kind_list, radius_list, y_list):
        b = NodeBrush(kind, ax)
        handler.add_node_sequence(token, n, offset=y, brush=b)

    for st, et in zip(token_list[:-1], token_list[1:]):
        eb = EdgeBrush('arrow', ax)
        handler.connecta2a(st, et, eb)
