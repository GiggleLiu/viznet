import numpy as np
from viznet import NodeBrush, DynamicShow, Layerwise, EdgeBrush


def test_draw_bm():
    '''Draw a Boltzmann Machine'''
    num_node_visible = 6
    with DynamicShow((5, 4), '_bm.png') as d:
        # define brushes
        node = NodeBrush('nn.backfed', d.ax, size='normal')
        edge = EdgeBrush('---', d.ax)

        node_list = add_circled_node_sequence(
            num_node_visible, node, radius=1.0, offset=(0, 0))

        # connect all
        for i, nodei in enumerate(node_list):
            # add text
            nodei.text(r'$\sigma_%d$' % i)
            for nodej in node_list:
                if nodei is not nodej:
                    edge >> (nodei, nodej)


def add_circled_node_sequence(num_node, brush, radius, offset=(0, 0)):
    '''
    add a sequence of nodes placed on a ring.

    Args:
        num_node (int): number of node to be added.
        brush (:obj:`NodeBrush`): node brush.
        radius (float): the raidus of the ring.
        offset (tuple|float): offset in x-y directions.

    Return:
        list: a list of nodes
    '''
    theta_list = np.arange(0, 2 * np.pi, 2 * np.pi / num_node)
    R = radius * num_node / np.pi
    xylist = np.array([np.cos(theta_list), np.sin(theta_list)]).T * R

    node_list = []
    i = 0
    for xy in xylist:
        node_list.append(brush >> xy)
        i += 1
    return node_list


if __name__ == '__main__':
    test_draw_bm()
