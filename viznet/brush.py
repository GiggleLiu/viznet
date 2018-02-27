import pdb
import numpy as np
import re
import matplotlib.pyplot as plt
from matplotlib import patches

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
        size ('huge'|'large'|'normal'|'small'|'tiny'|tuple|float): size of node.
    '''
    size_dict = {
        'huge': 0.9,
        'large': 0.39,
        'normal': 0.3,
        'small': 0.21,
        'tiny': 0.09,
    }

    def __init__(self, style, ax=None, color=None, size='normal', zorder=0):
        self.style = style
        self.size = size
        self.ax = ax
        self.color = color
        self.zorder = zorder

    @property
    def _size(self):
        if isinstance(self.size, str):
            size = self.size_dict[self.size]
        else:
            size = self.size
        return size

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
        # color priority: brush color > theme color
        color, geo, inner_geo = self._style
        if color is None:
            edgecolor = 'none'
        if self.color is not None:
            color = self.color
        ax = plt.gca() if self.ax is None else self.ax

        lw = node_setting['lw']
        edgecolor = node_setting['edgecolor']
        inner_fc = node_setting['inner_facecolor']
        inner_ec = node_setting['inner_edgecolor']
        inner_lw = node_setting['inner_lw']
        basesize = node_setting['basesize']

        # the size of node
        size = self._size
        if isinstance(size, tuple):
            if geo == 'rectangle':
                size = (size[0] * basesize, size[1] * basesize)
            else:
                raise
        elif geo == 'rectangle' and not isinstance(size, tuple):
            size = (size * basesize,) * 2
        else:
            size = size * basesize

        if color is None:
            color = 'none'
            edgecolor = 'none'

        if geo == 'circle':
            c = plt.Circle(xy, size, edgecolor=edgecolor,
                           facecolor=color, lw=lw, zorder=self.zorder)
        elif geo == 'square':
            xy = xy[0] - size, xy[1] - size
            c = plt.Rectangle(xy, 2 * size, 2 * size, edgecolor=edgecolor,
                              facecolor=color, lw=lw, zorder=self.zorder)
        elif geo[:8] == 'triangle':
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
            c = plt.Polygon(xy=tri_path * size + xy, edgecolor=edgecolor,
                            facecolor=color, lw=0.7, zorder=self.zorder)
        elif geo == 'diamond':
            dia_path = np.array([[-1, 0], [0, -1], [1, 0], [0, 1]])
            c = plt.Polygon(xy=dia_path * size + xy, edgecolor=edgecolor,
                            facecolor=color, lw=0.7, zorder=self.zorder)
        elif geo[:9] == 'rectangle' or geo[:9] == 'routangle':
            remain = geo[9:]
            match_res = re.match(r'-(\d)-(\d)', remain)
            if match_res:
                width = size * 2 + \
                    grid_setting['grid_width'] * (int(match_res.group(1)) - 1)
                height = size * 2 + \
                    grid_setting['grid_height'] * (int(match_res.group(2)) - 1)
            elif remain == '-golden':
                height = size * 2
                width = height * 1.3
            elif remain == '':
                width = size[0] * 2
                height = size[1] * 2
            else:
                raise
            xy_ = xy[0] - width / 2., xy[1] - height / 2.
            if geo[:9] == 'rectangle':
                c = plt.Rectangle(xy_, width, height, edgecolor=edgecolor,
                                  facecolor=color, lw=lw, zorder=self.zorder)
            else:
                pad = 0.15*min(width, height)
                c = patches.FancyBboxPatch(xy_+np.array([pad,pad]), width-pad*2, height-pad*2, zorder=self.zorder,
                                  edgecolor=edgecolor, facecolor=color, lw=lw,
                                  boxstyle=patches.BoxStyle("Round", pad=pad))
        elif geo == '':
            c = plt.Circle(xy, 0, edgecolor='none', facecolor='none')
        else:
            raise
        node = Node(c, self._style, ax=ax)
        ax.add_patch(c)

        # add a geometric patch at the top of circle.
        if inner_geo != 'none':
            if inner_geo == 'circle':
                g = plt.Circle(xy, 0.7 * size, edgecolor=inner_ec,
                               facecolor=inner_fc, lw=inner_lw, zorder=self.zorder+1)
                ax.add_patch(g)
            elif inner_geo == 'triangle':
                g = plt.Polygon(xy=np.array([[-0.5 * np.sqrt(3), -0.5], [0.5 * np.sqrt(3), -0.5], [
                    0, 1]]) * 0.7 * size + xy, edgecolor=inner_ec, facecolor=inner_fc, lw=inner_lw, zorder=self.zorder+1)
                ax.add_patch(g)
            elif inner_geo == 'dot':
                g = plt.Circle(xy, 0.15 * size, edgecolor=inner_ec,
                               facecolor=inner_ec, lw=inner_lw, zorder=self.zorder+1)
                ax.add_patch(g)
            elif inner_geo in ['cross', 'plus', 'vbar']:
                radi = size
                if inner_geo == 'plus':
                    sxy_list = [(xy[0] - radi, xy[1]), (xy[0], xy[1] - radi)]
                    exy_list = [(xy[0] + radi, xy[1]), (xy[0], xy[1] + radi)]
                elif inner_geo == 'vbar':
                    sxy_list = [(xy[0], xy[1] - radi)]
                    exy_list = [(xy[0], xy[1] + radi)]
                else:
                    radi_ = radi / np.sqrt(2.)
                    sxy_list = [(xy[0] - radi_, xy[1] - radi_),
                                (xy[0] + radi_, xy[1] - radi_)]
                    exy_list = [(xy[0] + radi_, xy[1] + radi_),
                                (xy[0] - radi_, xy[1] + radi_)]
                for sxy, exy in zip(sxy_list, exy_list):
                    plt.plot([sxy[0], exy[0]], [sxy[1], exy[1]],
                             color=inner_ec, lw=inner_lw, zorder=self.zorder+1)
            elif inner_geo == 'measure':
                sxy, exy = (xy[0], xy[1] - height * 0.4), (xy[0] +
                                                           width * 0.35, xy[1] + height * 0.35)
                plt.plot([sxy[0], exy[0]], [sxy[1], exy[1]],
                         color=inner_ec, lw=inner_lw, zorder=self.zorder+1)
                x = np.linspace(-width * 0.4, width * 0.4, 100)
                radi = height * 0.5
                y = radi**2 - x**2
                plt.plot(x + xy[0], y + xy[1] - radi * 0.4,
                         color=inner_ec, lw=inner_lw, zorder=self.zorder+1)
            else:
                raise ValueError('Inner Geometry %s not defined!' % geo)

        # for BLUE nodes, add a self-loop (Stands for Recurrent Unit)
        if color == BLUE and self.style[:3] == 'nn.':
            loop = plt.Circle((xy[0], xy[1] + 1.2 * size), 0.5 * size,
                              edgecolor=edgecolor, facecolor=inner_fc, lw=lw, zorder=-5)
            ax.add_patch(loop)

        return node


class EdgeBrush(Brush):
    '''
    a brush for drawing edges.

    Attributes:
        style (str): the style of edge, must be a combination of ('>'|'<'|'-'|'.').
            * '>', right arrow
            * '<', left arrow,
            * '-', line,
            * '.', dashed line.
        ax (:obj:`Axes`): matplotlib Axes instance.
        lw (float): line width.
        color (str): the color of painted edge by this brush.
    '''

    def __init__(self, style, ax=None, lw=1, color='k', zorder=0):
        self.lw = lw
        self.color = color
        self.ax = ax
        self.style = style
        self.zorder = zorder

    def __rshift__(self, startend):
        '''
        connect start node and end node

        Args:
            startend (tuple): start node and end node.

        Returns:
            :obj:`Edge`: edge object.
        '''
        ax = plt.gca() if self.ax is None else self.ax
        lw = self.lw
        head_length = arrow_setting['head_length'] * lw
        head_width = arrow_setting['head_width'] * lw
        edge_ratio = arrow_setting['edge_ratio']
        start, end = startend
        sxy, exy = np.array(start.position), np.array(end.position)
        d = exy - sxy
        unit_d = d / np.linalg.norm(d)
        sxy = start.get_connection_point(unit_d)
        exy = end.get_connection_point(-unit_d)
        d = np.asarray(exy) - sxy
        unit_d = d / np.linalg.norm(d)

        # get arrow locations.
        arrow_locs = []
        segs = []
        for s in self.style:
            if s in ['>', '<']:
                arrow_locs.append([s, len(segs)])
            else:
                segs.append(s)
        head_vec = unit_d * head_length
        vec_d = d - head_vec * 1.2
        num_segs = len(segs)
        for al in arrow_locs:
            al[1] = al[1] * vec_d / max(num_segs, 1) + sxy + 0.6 * head_vec
        # show the arrow
        for st, mxy in arrow_locs:
            sign = 1 if st == '>' else -1
            mxy = mxy - sign * head_vec * 0.6
            plt.arrow(mxy[0], mxy[1], sign * 1e-8 * d[0], sign * 1e-8 * d[1],
                      head_length=head_length, width=0,
                      head_width=head_width, fc=self.color,
                      length_includes_head=False, lw=lw, edgecolor=self.color, zorder=self.zorder)

        # get the line locations.
        uni = d / num_segs
        lines = []
        end = start = sxy
        seg_pre = ''
        for seg in segs:
            if seg != seg_pre and seg_pre != '':
                lines.append([seg_pre, start, end])
                start = end
            seg_pre = seg
            end = end + uni
        lines.append([seg, start, end])
        # fix end of line
        if self.style[-1] in ['<', '>']:
            lines[-1][2] -= head_vec
        if self.style[0] in ['<', '>']:
            lines[0][1] += head_vec

        # show the lines.
        for ls, sxy, exy in lines:
            if ls == '=':
                perp_d = np.array([-unit_d[1], unit_d[0]])
                offset = perp_d * head_width * 0.4
                sxys = [(sxy + offset, exy + offset),
                        (sxy - offset, exy - offset)]
                ls = '-'
            else:
                sxys = [(sxy, exy)]
            if ls == '.':
                ls = '--'
            for sxy_, exy_ in sxys:
                arr = ax.plot([sxy_[0], exy_[0]], [
                                   sxy_[1], exy_[1]], lw=lw, color=self.color,
                                   zorder=self.zorder, ls=ls, solid_capstyle='round')

        return Edge(arr, sxy, exy, start, end, ax=ax)

def _arrow_loc(lines, segs):
    pass
