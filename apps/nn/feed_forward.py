'''
Plots for zoo of nets.
'''

import numpy as np
from viznet import Layerwise, NodeBrush, EdgeBrush, DynamicShow

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
        handler.node_sequence(token, n, offset=y, brush=b)

    for st, et in zip(token_list[:-1], token_list[1:]):
        eb = EdgeBrush('-->', ax)
        handler.connecta2a(st, et, eb)


def real_bp():
    with DynamicShow((6, 6), '_feed_forward.png') as d:
        draw_feed_forward(d.ax, num_node_list=[5, 4, 1])

if __name__ == '__main__':
    real_bp()
