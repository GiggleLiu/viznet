from __future__ import division

import pdb
import numpy as np
from matplotlib import pyplot as plt

from ..layerwise import *
from ..context import DynamicShow
from ..theme import NODE_THEME_DICT
from ..brush import *
from ..zoo import *


def test_draw_rbm():
    plt.ion()
    fig = plt.figure(figsize=(6, 4))
    ax = plt.gca()
    draw_rbm(ax, 5, 4)
    ax.axis('equal')
    ax.axis('off')

    pdb.set_trace()
    plt.savefig('_rbm_test.png')


def test_draw_rbm_equivalent():
    with DynamicShow((6, 4), '_rbm_test.png') as d:
        draw_rbm(d.ax, 5, 4)


def test_draw_feed_forward():
    with DynamicShow((6, 6), '_feed_forward.png') as d:
        draw_feed_forward(d.ax, num_node_list=[5, 4, 1])


def test_theme_table():
    '''plot a table of node themes'''
    genre = [('nn.', 'nn'), ('tn.', 'tn'), ('qc.','qc'), ('', '')]
    for head, token in genre:
        with DynamicShow((11, 6), filename='_%s_theme_list.png' % token) as d:
            handler = Layerwise()
            i = 0
            for kind in NODE_THEME_DICT.keys():
                if kind[:3] == head or (kind[:3] not in ['nn.', 'tn.', 'qc.'] and token == ''):
                    brush = NodeBrush(kind, d.ax)
                    node = brush >> (i%5, -(i // 5))
                    node.text(kind, 'bottom')
                    i += 1


if __name__ == '__main__':
    test_theme_table()
    test_draw_feed_forward()
    test_draw_rbm()
    test_draw_rbm_equivalent()
