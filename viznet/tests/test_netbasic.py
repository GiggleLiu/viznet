from __future__ import division

import pdb
import numpy as np
from matplotlib import pyplot as plt

from ..context import DynamicShow
from ..theme import NODE_THEME_DICT
from ..brush import *


def test_theme_table():
    '''plot a table of node themes'''
    genre = [('nn.', 'nn'), ('tn.', 'tn'), ('qc.', 'qc'), ('', '')]
    for head, token in genre:
        with DynamicShow((11, 6), filename='_%s_theme_list.png' % token) as d:
            i = 0
            for kind in NODE_THEME_DICT.keys():
                if kind[:3] == head or (kind[:3] not in ['nn.', 'tn.', 'qc.'] and token == ''):
                    brush = NodeBrush(kind, d.ax)
                    node = brush >> (i % 5, -(i // 5))
                    node.text(kind, 'bottom')
                    i += 1


if __name__ == '__main__':
    test_theme_table()
