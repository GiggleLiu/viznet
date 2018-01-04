import pdb
import numpy as np
from matplotlib import pyplot as plt

from viznet import *


def test_draw_rbm():
    num_node_visible = 5
    num_node_hidden = 4
    with DynamicShow((6, 4), '_rbm.pdf') as d:
        handler = Layerwise()
        # visible layers
        nb1 = NodeBrush('nn.backfed', d.ax)
        nb2 = NodeBrush('nn.probablistic_hidden', d.ax)
        eb = EdgeBrush('undirected', d.ax)

        handler.node_sequence(
            '\sigma^z', num_node_visible, offset=0, brush=nb1)

        # hidden layers
        handler.node_sequence('h', num_node_hidden, offset=1, brush=nb2)

        # automatic text node sequence
        handler.text('h')
        handler.text('\sigma^z')

        # connect them
        handler.connecta2a('\sigma^z', 'h', eb)


if __name__ == '__main__':
    test_draw_rbm()
