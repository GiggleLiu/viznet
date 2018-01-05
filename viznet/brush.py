import pdb
import numpy as np
import re
import matplotlib.pyplot as plt

from .edgenode import Edge, Node
from .theme import NODE_THEME_DICT, BLUE
from .utils import rotate
from .setting import node_setting, arrow_setting, grid_setting


class Brush(object):
    pass


class NodeBrush(Brush):
    '''
    a brush class used to draw node.

    Attributes:
        style (str): refer keys for `viznet.theme.NODE_THEME_DICT`.
        ax (:obj:`Axes`): matplotlib Axes instance.
        color (str|None): the color of painted node by this brush, it will overide theme color if is not `None`.
        size ('huge'|'large'|'normal'|'small'|'tiny'): size of node.
    '''
    size_dict = {
        'huge': 3,
        'large': 1.3,
        'normal': 1.0,
        'small': 0.7,
        'tiny': 0.3,
    }

    def __init__(self, style, ax, color=None, size='normal'):
        self.style = style
        self.size = size
        self.ax = ax
        self.color = color

    @property
    def _size(self):
        return self.size_dict[self.size]

    @property
    def _style(self):
        return NODE_THEME_DICT[self.style]

    def __rshift__(self, xy):
        '''
        add a node.

        Args:
            xy (tuple): position.

        Returns:
            :obj:`Node`: node object.
        '''
        basesize = 0.3
        # color priority: brush color > theme color
        color, geo, inner_geo = self._style
        if self.color is not None:
            color = self.color

        lw = node_setting['lw']
        edgecolor = node_setting['edgecolor']
        inner_fc = node_setting['inner_facecolor']
        inner_ec = node_setting['inner_edgecolor']
        inner_lw = node_setting['inner_lw']
        size = self._size

        if color is None:
            color = 'none'
            edgecolor = 'none'

        if geo == 'circle':
            c = plt.Circle(xy, basesize * size, edgecolor=edgecolor,
                           facecolor=color, lw=lw, zorder=0)
        elif geo == 'square':
            a = size * 2 * basesize
            xy = xy[0] - a / 2., xy[1] - a / 2.
            c = plt.Rectangle(xy, a, a, edgecolor=edgecolor,
                              facecolor=color, lw=lw, zorder=0)
        elif geo[:8] == 'triangle':
            r = size * basesize
            tri_path = np.array(
                [[-0.5 * np.sqrt(3), -0.5], [0.5 * np.sqrt(3), -0.5], [0, 1]])
            if geo == 'triangle-d':
                tri_path = rotate(tri_path, np.pi)
            elif geo == 'triangle-l':
                tri_path = rotate(tri_path, np.pi / 2.)
            elif geo == 'triangle-r':
                tri_path = rotate(tri_path, -np.pi / 2.)
            elif geo == 'triangle-u' or 'triangle':
                pass
            else:
                raise
            c = plt.Polygon(xy=tri_path * r + xy, edgecolor=edgecolor,
                            facecolor=color, lw=0.7, zorder=0)
        elif geo[:9] == 'rectangle':
            match_res = re.match(r'rectangle-(\d)-(\d)', geo)
            width = size * 2 * basesize + \
                grid_setting['grid_width'] * (int(match_res.group(1)) - 1)
            height = size * 2 * basesize + \
                grid_setting['grid_height'] * (int(match_res.group(2)) - 1)
            xy = xy[0] - width / 2., xy[1] - height / 2.
            c = plt.Rectangle(xy, width, height, edgecolor=edgecolor,
                              facecolor=color, lw=lw, zorder=0)
        else:
            raise
        self.ax.add_patch(c)

        # add a geometric patch at the top of circle.
        if inner_geo != 'none':
            if inner_geo == 'circle':
                g = plt.Circle(xy, 0.7 * basesize * size, edgecolor=inner_ec,
                               facecolor=inner_fc, lw=inner_lw, zorder=101)
            elif inner_geo == 'triangle':
                g = plt.Polygon(xy=np.array([[-0.5 * np.sqrt(3), -0.5], [0.5 * np.sqrt(3), -0.5], [
                    0, 1]]) * 0.7 * basesize * size + xy, edgecolor=inner_ec, facecolor=inner_fc, lw=inner_lw, zorder=101)
            else:
                raise ValueError('Inner Geometry %s not defined!' % geo)
            self.ax.add_patch(g)

        # for BLUE nodes, add a self-loop (Stands for Recurrent Unit)
        if color == BLUE and self.style[:3] == 'nn.':
            loop = plt.Circle((xy[0], xy[1] + 1.2 * basesize * size), 0.5 * basesize * size,
                              edgecolor=edgecolor, facecolor=inner_fc, lw=lw, zorder=-5)
            self.ax.add_patch(loop)

        return Node(c, self._style, ax=self.ax)


class EdgeBrush(Brush):
    '''
    a brush for drawing edges.

    Attributes:
        style (str): the style of edge, currrently ('directed'|'undirected'|'arrow') are available.
        ax (:obj:`Axes`): matplotlib Axes instance.
        lw (float): line width.
        color (str): the color of painted edge by this brush.
    '''

    def __init__(self, style, ax, lw=1, color='k'):
        self.lw = lw
        self.color = color
        self.ax = ax
        self.style = style

    def __rshift__(self, startend):
        '''
        connect start node and end node

        Args:
            startend (tuple): start node and end node.

        Returns:
            :obj:`Edge`: edge object.
        '''
        lw = self.lw
        head_length = arrow_setting['head_length'] * lw
        head_width = arrow_setting['head_width'] * lw
        start, end = startend
        sxy, exy = np.array(start.position), np.array(end.position)
        d = exy - sxy
        unit_d = d / np.linalg.norm(d)
        sxy = start.get_connection_point(unit_d)
        exy = end.get_connection_point(-unit_d)
        d = exy - sxy
        # arr = self.ax.arrow(sxy[0], sxy[1], d[0], d[1],
        #                    head_length=head_length if self.style=='arrow' else 0, width=0.015*lw,
        #                    head_width=head_width, fc=self.color,
        #                    length_includes_head=True, lw=0, edgecolor='none')

        # show the arrow
        if self.style in ['directed', 'arrow']:
            head_vec = unit_d * head_length
            if self.style == 'directed':
                mxy = sxy + d / 2. - head_vec / 2.
            else:
                head_vec = head_length * unit_d
                exy = exy - head_vec * 1.3
                mxy = exy
            plt.arrow(mxy[0], mxy[1], 0.01 * d[0], 0.01 * d[1],
                      head_length=head_length, width=0,
                      head_width=head_width, fc=self.color,
                      length_includes_head=False, lw=lw, edgecolor=self.color)
        # show the line
        arr = self.ax.plot([sxy[0], exy[0]], [
                           sxy[1], exy[1]], lw=lw, color=self.color)

        return Edge(arr, sxy, exy, start, end, ax=self.ax)
