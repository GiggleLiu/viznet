'''
back propagation.
'''

import matplotlib.pyplot as plt

from ..netbasic import *
from .convrbm import draw_conv_rbm

def real_bp():
    with DynamicShow((6, 6), '_feed_forward.png') as d:
        draw_feed_forward(d.ax, num_node_list=[5, 4, 1])

