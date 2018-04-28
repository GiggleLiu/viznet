'''
Basic plotlib for neural networks.

feature list:
    1. draw nodes with label.
    2. draw directed/undirected links between two nodes by node labels.
    3. implementation of simple RBM and Feed forward networks.
'''

import numpy as np
import pdb
import numbers
from matplotlib import pyplot as plt
from matplotlib.patches import Circle, Polygon

from .edgenode import Pin
from .brush import EdgeBrush, NodeBrush

__all__ = ['QuantumCircuit']


class QuantumCircuit(object):
    '''
    Args:
        ax: matplotlib.pyplot.Axes.
        num_bit (int): number of bits.
        y0 (float): the y offset.
    '''
    line_space = 1.0

    def __init__(self, num_bit, ax=None, x=0, y0=0, **kwargs):
        self.x = x
        self.y0 = y0
        self.node_dict = dict(
            zip(range(num_bit), [[Pin(self.get_position(i))] for i in range(num_bit)]))
        self.edge = EdgeBrush('---', ax, **kwargs)

    @property
    def num_bit(self):
        return len(self.node_dict)

    def get_position(self, line, x=None):
        '''get the position of specific line'''
        if x is None: x=self.x
        return (x, self.y0-line*self.line_space)

    def gate(self, brush, position, text=None, fontsize=18):
        '''
        place a gate at specific position.
        '''
        if not hasattr(brush, '__len__'):
            brush = (brush,)
            return_list = False
        else:
            return_list = True
        if not hasattr(position, '__len__'):
            position = (position,)
        if len(brush) == 1 and len(position) > 1:
            position_node = (np.mean(position),)
        elif len(brush) > 1 and len(position) > 1 and len(brush) != len(position):
            raise ValueError()
        else:
            position_node = position

        node_list = []
        for b, y in zip(brush, position_node):
            node = b >> self.get_position(y)

            # connect nodes
            if len(node_list) >= 1:
                self.edge >> (node_list[-1], node)
            if position_node is position:
                self.edge >> (self.node_dict[y][-1], node)
                self.node_dict[y].append(node)
            else:
                for y in position:
                    prenode = self.node_dict[y][-1]
                    lnode = node.pin('left', align=prenode)
                    rnode = node.pin('right', align=prenode)
                    self.node_dict[y].append(lnode)
                    self.node_dict[y].append(rnode)
                    self.edge >> (prenode, lnode)
            node_list.append(node)

        if text is not None:
            node.text(text, fontsize=fontsize)
        return node_list if return_list else node_list[0]

    def block(self, boxbrush, linestart, lineend, pad_x=0.35, pad_y=0.35):
        '''
        strike out a block.

        Args:
            boxbrush (NodeBrush): a brush of style 'box', 'art.rbox' or something rectangular.
            linestart (int): the starting line.
            lineend (int): the ending line > starting line.
            pad_x (float): x padding between gates and box.
            pad_y (float): y padding between gates and box.

        Returns:
            context: context that return boxes.
        '''
        class Context():
            def __enter__(ctx, *args):
                ctx.xstart = self.x
                self.boxes = []
                return self.boxes

            def __exit__(ctx, type, value, tb):
                if tb is not None:
                    print(tb)
                    return False
                xend = self.x
                xstart = ctx.xstart
                boxbrush.size = ((xend - xstart)/2. + pad_x, (lineend - linestart)/2.*self.line_space + pad_y)
                b = boxbrush >> ((xstart+xend)/2., -(linestart + lineend)/2.*self.line_space)
                self.boxes.append(b)
                return True
        return Context()

    def focus(self, lines):
        '''
        focus to target lines

        Args:
            lines (list): the target lines to put up.
        '''
        alllines = range(self.num_bit)
        pin = NodeBrush('pin')
        old_positions = []
        for i in range(self.num_bit):
            old_positions.append(self.gate(pin, i))

        lmap = np.append(lines, np.setdiff1d(alllines, lines))
        self.x += 0.8
        pins = []
        for opos, j in zip(old_positions, lmap):
            pi = Pin(self.get_position(j))
            self.node_dict[j].append(pi)
            self.edge >> (opos, pi)
            pins.append(pi)
        return pins

    def boxbrush(self, num_line, style='qc.box', width=0.5, **kwargs):
        '''
        create a box brush that across multiple lines.

        Args:
            num_line (int): number of lines.
            width (float): the width.
        '''
        bb = NodeBrush(style, size=(width, (num_line-1)*self.line_space/2.+0.3), **kwargs)
        return bb
