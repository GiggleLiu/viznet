import pdb
import numpy as np
from matplotlib import pyplot as plt

from viznet import *


def test_draw_rbm():
    num_node_visible = 5
    num_node_hidden = 4
    with DynamicShow((6, 4), '_rbm.pdf') as d:
        # visible layers
        nb1 = NodeBrush('nn.backfed', d.ax)
        nb2 = NodeBrush('nn.probablistic_hidden', d.ax)
        eb = EdgeBrush('---', d.ax)

        sigma = node_sequence(nb1, num_node_visible, center=(0, 0))

        # hidden layers
        h = node_sequence(nb2, num_node_hidden, center=(0, 1))

        # text node sequence
        for i, node in enumerate(h):
            node.text(r'$h_%d$'%i)
        for i, node in enumerate(sigma):
            node.text(r'$\sigma^z_%d$'%i)

        # connect them
        connecta2a(sigma, h, eb)


if __name__ == '__main__':
    test_draw_rbm()
