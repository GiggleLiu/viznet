import pdb
import numpy as np
from matplotlib import pyplot as plt

from ..netbasic import *
from ..zoo import *


def test_draw_bm():
    num_node_visible = 6
    with DynamicShow((5, 4), '_bm.pdf') as d:
        handler = NNPlot(d.ax)
        add_circled_node_sequence(handler, num_node_visible, token='\sigma^z', offset=(0,0), kind='backfed', radius=0.3, show_name=True)
        # visible layers
        handler.connect_layers('\sigma^z', '\sigma^z', False)

def add_circled_node_sequence(handler, num_node, token, offset=(0,0), kind='basic', radius=0.2,
        show_name=True):
    '''
    add a sequence of nodes along x-direction.

    Args:
        num_node (int): number of node to be added.
        token (int): the token to name this serie of nodes. e.g. token 'x' will generate node serie `$x_1$, $x_2$ ...`.
        offset (tuple|float): offset in x-y directions. if a number is passed, offset along perpendicular direction with respect to :data:`handler.distance`.
        kind (str, default='basic'): the kind of node, see `NODE_THEME_DICT` for reference.
        radius (float, default=0.2): the size of ball.
        show_name (str|bool, default=True): display the name of each node, if str provided, display string.

    Return:
        list: a list of node names, you can visit this node by accesing `handler.node_dict[node_name]`.
    '''
    theta_list = np.arange(0, 2*np.pi, 2*np.pi/num_node)
    R = np.linalg.norm(handler.distance)*num_node/np.pi
    xylist = np.array([np.cos(theta_list), np.sin(theta_list)]).T*R
    return handler._add_node_sequence(xylist, token, offset, kind, radius, show_name)


if __name__ == '__main__':
    test_draw_bm()
