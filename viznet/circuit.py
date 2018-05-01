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
        if isinstance(line, slice):
            return (x, slice(self.get_position(line.start)[1], self.get_position(line.stop)[1]))
        else:
            return (x, self.y0-line*self.line_space)

    def gate(self, brush, position, text='', fontsize=18):
        '''
        place a gate at specific position.
        '''
        if not hasattr(brush, '__len__'):
            brush = [brush]
            position = [position]
            text = [text]
            return_list = False
        else:
            return_list = True
            if not isinstance(text, (list, tuple)):
                text = [text]*len(brush)
        if len(brush) != len(position) or len(text)!=len(brush):
            raise ValueError('number of gate-position-text mismatch!')
        line_all = list(range(self.num_bit))

        node_list = []
        for b, line, t in zip(brush, position, text):
            # get the position to place bits, and the aplied bits.
            if isinstance(line, slice):
                y = (line.stop + line.start)/2.
                line = line_all[line.start: line.stop+1]
            if hasattr(line, '__len__'):
                if len(line) == 1:
                    line = y = line[0]
                else:
                    y = slice(min(line),max(line))
            else:
                y = line

            # place the node
            node = b >> self.get_position(y)

            # connect nodes
            if len(node_list) >= 1:
                self.edge >> (node_list[-1], node)
            if not isinstance(y, slice):
                self.edge >> (self.node_dict[line][-1], node)
                self.node_dict[line].append(node)
            else:
                for yline in line:
                    prenode = self.node_dict[yline][-1]
                    lnode = node.pin('left', align=prenode)
                    rnode = node.pin('right', align=prenode)
                    self.node_dict[yline].append(lnode)
                    self.node_dict[yline].append(rnode)
                    self.edge >> (prenode, lnode)
            node_list.append(node)

            # text node
            if text != '':
                node.text(t, fontsize=fontsize)
        return node_list if return_list else node_list[0]

    def block(self, sls, pad_x=0.35, pad_y=0.35, brush=None):
        '''
        strike out a block.

        Args:
            sls (int): the slice for starting and ending lines.
            pad_x (float): x padding between gates and box.
            pad_y (float): y padding between gates and box.
            brush (NodeBrush|None): the brush used to paint this box.

        Returns:
            context: context that return boxes.
        '''
        if brush is None: brush = NodeBrush('box', ls='--', roundness=0.2)
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
                b = brush >> (slice(xstart-pad_x, xend+pad_x), slice(self.get_position(sls.start)[1], self.get_position(sls.stop)[1]))
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
