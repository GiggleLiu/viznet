import pdb
import numpy as np
from matplotlib import pyplot as plt

from ..netbasic import *
from ..zoo import *


def test_draw_rbm():
    num_node_visible = 5
    num_node_hidden = 4
    with DynamicShow((6, 4), '_rbm.png') as d:
        handler = NNPlot(d.ax)
        # visible layers
        handler.add_node_sequence(
            num_node_visible, '\sigma^z', 0, kind='backfed', radius=0.3)
        # hidden layers
        handler.add_node_sequence(num_node_hidden, 'h',
                                  1.5, kind='probablistic_hidden', radius=0.3)
        # connect them
        handler.connect_layers('\sigma^z', 'h', False)


if __name__ == '__main__':
    test_draw_rbm()
