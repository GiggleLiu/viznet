'''
Basic plotlib for neural networks.

feature list:
    1. draw nodes with label.
    2. draw directed/undirected links between two nodes by node labels.
    3. implementation of simple RBM and Feed forward networks.
'''

import numpy as np
import pdb

__all__ = ['node_sequence', 'node_ring', 'connect121', 'connecta2a', 'text_cluster']


def node_sequence(brush, num_node, center, space=(1,0)):
    '''
    add a sequence of nodes along direction specified by space.

    Args:
        brush (NodeBrush): brush instance.
        num_node (int): number of node to be added.
        center (tuple): center of this sequence.
        space (tuple|float): space between nodes.

    Return:
        list: a list of node names, you can visit this node by accesing `self.node_dict[node_name]`.
    '''
    x_list = np.arange(-num_node / 2. + 0.5, num_node / 2., 1)
    xylist = center + np.asarray(space) * x_list[:, None]

    node_list = []
    for i, xy in enumerate(zip(xylist[:, 0], xylist[:, 1])):
        node_list.append(brush >> xy)
    return node_list

def connect121(start_nodes, end_nodes, brush):
    '''
    Args:
        start_token (str): the start layer generation token (pointed from).
        end_token (str): the end layer generation token (pointed to).
        brush (EdgeBrush): edge brush instance.
    '''
    return _connect(start_nodes, end_nodes, brush, one2one=True)

def connecta2a(start_nodes, end_nodes, brush):
    '''
    Args:
        start_token (str): the start layer generation token (pointed from).
        end_token (str): the end layer generation token (pointed to).
        brush (EdgeBrush): edge brush instance.
    '''
    return _connect(start_nodes, end_nodes, brush, one2one=False)

def _connect(start_nodes, end_nodes, brush, one2one=False):
    edge_list = []
    for i, start_node in enumerate(start_nodes):
        if one2one:
            edge_list.append(brush >> (start_node, end_nodes[i]))
        else:
            for end_node in end_nodes:
                edge_list.append(brush >> (start_node, end_node))
    return edge_list

def text_cluster(node_list, token, *args, **kwargs):
    '''
    add texts for a sequence of nodes.

    Args:
        node_list (list): a list of nodes.
        text (str): automatically text.
    '''
    def _autoname(token, i):
        return r'$%s_%d$'%(token, i)

    # use auto name
    text_list = [_autoname(token, i)
                 for i in range(len(node_list))]
    for node, text in zip(node_list, text_list):
        node.text(text, *args, **kwargs)

def node_ring(brush, num_node, center, radius):
    '''
    add a sequence of nodes placed on a ring.

    Args:
        brush (:obj:`NodeBrush`): node brush.
        num_node (int): number of node to be added.
        center (tuple): center of this ring.
        radius (float): the raidus of the ring.

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
