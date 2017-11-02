import pdb
import numpy as np
from matplotlib import pyplot as plt

from ..netbasic import *

def test_draw_rbm():
    plt.ion()
    fig = plt.figure(figsize=(6, 4))
    ax = plt.gca()
    draw_rbm(ax, 5, 4)
    ax.axis('equal')
    ax.axis('off')

    pdb.set_trace()
    plt.savefig('_rbm.png')


def test_draw_feed_forward():
    plt.ion()
    fig = plt.figure(figsize=(6, 4))
    ax = plt.gca()
    draw_feed_forward(ax, num_node_list=[5, 4, 1])
    ax.axis('equal')
    ax.axis('off')

    pdb.set_trace()
    plt.savefig('_feed_forward.png')


if __name__ == '__main__':
    test_draw_rbm()
    test_draw_feed_forward()
