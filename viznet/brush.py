import pdb
import numbers
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import patches, transforms
from matplotlib.path import Path
from numpy.linalg import norm

from .edgenode import Edge, Node, Pin
from .theme import NODE_THEME_DICT, BLUE
from .utils import rotate
from .setting import node_setting, edge_setting

__all__ = ['Brush', 'NodeBrush', 'EdgeBrush', 'CLinkBrush']

class Brush(object):
    '''Base Class of brushes.'''
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
    setting = node_setting

    size_dict = {
        'huge': 0.9,
        'large': 0.39,
        'normal': 0.3,
        'small': 0.21,
        'tiny': 0.09,
    }

    def __init__(self, style, ax=None, color=None, size='normal', zorder=0, rotate=0., ls='-'):
        self.style = style
        self.size = size
        self.ax = ax
        self.color = color
        self.zorder = zorder
        self.rotate = rotate
        self.ls = ls
        self.node_handler = basicgeometry_handler

    @property
    def _size(self):
        if isinstance(self.size, str):
            size = self.size_dict[self.size]
        else:
            size = self.size
        return np.asarray(size)

    def __rshift__(self, xy):
        '''
        add a node.

        Args:
            xy (tuple): position.

        Returns:
            :obj:`Node`: node object.
        '''
        # color priority: brush color > theme color
        ax = plt.gca() if self.ax is None else self.ax
        lw = self.setting['lw']
        edgecolor = self.setting['edgecolor']
        inner_fc = self.setting['inner_facecolor']
        inner_ec = self.setting['inner_edgecolor']
        inner_lw = self.setting['inner_lw']
        basesize = self.setting['basesize']
        # override color
        if self.color is not None:
            color = self.color

        theme_code = self._style
        objs = self.node_handler(theme_code, xy, basesize*self._size, self.color, edgecolor, lw, self.ls, self.zorder, self.rotate, inner_lw, inner_ec, inner_fc)

        # add patches
        for p in objs:
            ax.add_patch(p)
        node = Node(objs, theme_code)
        return node

    @property
    def _style(self):
        return NODE_THEME_DICT[self.style]


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
    setting = edge_setting

    def __init__(self, style, ax=None, lw=1, color='k', zorder=0):
        self.lw = lw
        self.color = color
        self.ax = ax
        self.style = style
        self.zorder = zorder
        self.line_handler = basicline_handler

    def __rshift__(self, startend):
        '''
        connect start node and end node

        Args:
            startend (tuple): start node (position) and end node (position).

        Returns:
            :obj:`Edge`: edge object.
        '''
        ax = plt.gca() if self.ax is None else self.ax
        lw = self.lw
        head_length = self.setting['arrow_head_length'] * lw
        head_width = self.setting['arrow_head_width'] * lw

        # get start position and end position
        start, end = startend
        if isinstance(start, tuple):
            start = Pin(start)
        if isinstance(end, tuple):
            end = Pin(end)
        sxy, exy = np.asarray(start.position), np.asarray(end.position)
        d = exy - sxy
        unit_d = d / norm(d)
        sxy = start.get_connection_point(unit_d)
        exy = end.get_connection_point(-unit_d)

        arrows, lines = self.line_handler(sxy, exy, self.style, head_length)
        objs = _arrows(ax, arrows, head_width=head_width, head_length=head_length, lw=lw, zorder=self.zorder, color=self.color)
        objs += _lines(ax, lines, lw=lw, color=self.color, zorder=self.zorder, use_path=False)
        return Edge(objs, sxy, exy, start, end, ax=ax)

class CLinkBrush(EdgeBrush):
    '''
    Brush for C type link.

    Attributes:
        style (str): e.g. '<->', right-side grow with respect to the line direction.
    '''
    def __init__(self, style, ax=None, offsets=(0.2,), roundness=0, lw=1, color='k', zorder=0):
        super(CLinkBrush, self).__init__(style, ax=ax, lw=lw, color=color, zorder=zorder)
        self.roundness = roundness
        self.offsets = list(offsets)
        self.line_handler = clink_handler

    def __rshift__(self, startend):
        '''
        connect start node and end node

        Args:
            startend (tuple): start node (position) and end node (position).

        Returns:
            :obj:`Edge`: edge object.
        '''
        ax = plt.gca() if self.ax is None else self.ax
        lw = self.lw
        head_length = self.setting['arrow_head_length'] * lw
        head_width = self.setting['arrow_head_width'] * lw

        # get start position and end position
        start, end = startend
        if isinstance(start, tuple):
            start = Pin(start)
        if isinstance(end, tuple):
            end = Pin(end)
        sxy, exy = np.asarray(start.position), np.asarray(end.position)

        arrows, lines, (sxy_, exy_) = self.line_handler(sxy, exy, self.style, self.offsets, self.roundness, head_length)
        objs = _arrows(ax, arrows, head_width=head_width, head_length=head_length, lw=lw, zorder=self.zorder, color=self.color)
        objs += _lines(ax, lines, lw=lw, color=self.color, zorder=self.zorder, use_path=True)
        return Edge(objs, sxy_, exy_, start, end, ax=ax)

def clink_handler(sxy, exy, style, offsets, roundness, head_length):
    '''a C style link between two edges.'''
    nturn = len(offsets)
    offsets = np.asarray(offsets)
    unit_t = (exy - sxy)/norm(exy - sxy)
    unit_l = rotate(unit_t, np.pi/2.)
    vl, vr = [sxy], [exy]

    # get arrow locations and directions
    # - first, get head and tail vector.
    arrows = []
    unit_head_vec = (-unit_t if nturn%2==0 else unit_l)*(np.sign(offsets[0]) if len(offsets)!=0 else -1)
    sign_eo = -1 if nturn%2 == 0 else 1
    unit_tail_vec = unit_head_vec * sign_eo
    head_vec = unit_head_vec * head_length
    tail_vec = unit_tail_vec * head_length
    if style[0] in ['<', '>']:
        sign = (1 if style[0]=='>' else -1)
        arrows.append((sxy+head_vec*0.6, unit_head_vec * sign))
        style = style[1:]
        vl[0] = vl[0] + head_vec
    if style[-1] in ['<', '>']:
        sign = (-1 if style[-1]=='>' else 1)
        arrows.append((exy+tail_vec*0.6, unit_tail_vec * sign))
        style = style[:-1]
        vr[0] = vr[0] + tail_vec

    # get path
    ls = style
    if len(ls) !=1:
        raise ValueError('style must contain exactly 1 line style code.')
    for i, dxy in enumerate(offsets):
        sxy = sxy + (-unit_t if i%2 == nturn%2 else unit_l)*dxy
        exy = exy + (unit_t if i%2 == nturn%2 else unit_l)*dxy
        vl.append(sxy)
        vr.append(exy)
    return arrows, [(ls, rounded_path(vl+vr[::-1], roundness))], (vl[-1], vr[-1])

def rounded_path(vertices, roundness):
    '''make rounded path from vertices.'''
    vertices = np.asarray(vertices)
    if roundness == 0:
        return Path(vertices)

    codes = [Path.MOVETO]
    vertices_new = [vertices[0]]
    for pre, cur, nex in zip(vertices[:-2], vertices[1:-1], vertices[2:]):
        codes.extend([Path.LINETO, Path.CURVE3, Path.CURVE3])
        dv_pre = (pre - cur)/norm(cur-pre)*roundness
        dv_nex = (nex - cur)/norm(cur-nex)*roundness
        vertices_new.extend([cur+dv_pre,cur,cur+dv_nex])
    codes.append(Path.LINETO)
    vertices_new.append(vertices[-1])
    return Path(vertices_new, codes)

def basicline_handler(sxy, exy, style, head_length):
    '''draw a line between start and end.'''
    # the distance and unit distance
    d = np.asarray(exy) - sxy
    unit_d = d / norm(d)

    # get arrow locations.
    arrows = []
    segs = []
    for s in style:
        if s in ['>', '<']:
            sign = 1 if s == '>' else -1
            arrows.append([len(segs), sign*unit_d])
        else:
            segs.append(s)
    head_vec = unit_d * head_length
    vec_d = d - head_vec * 1.2
    num_segs = len(segs)
    for al in arrows:
        al[0] = al[0] * vec_d / max(num_segs, 1) + sxy + 0.6 * head_vec

    # get the line locations.
    uni = d / num_segs
    lines = []
    end = start = sxy
    seg_pre = ''
    for seg in segs:
        if seg != seg_pre and seg_pre != '':
            lines.append([seg_pre, [start, end]])
            start = end
        seg_pre = seg
        end = end + uni
    lines.append([seg, [start, end]])

    # fix end of line
    if style[-1] in ['<', '>']:
        lines[-1][1][1] -= head_vec
    if style[0] in ['<', '>']:
        lines[0][1][0] += head_vec
    return arrows, lines

def _arrows(ax, arrows, **kwargs):
    '''show arrows'''
    objs = []
    for mxy, direction in arrows:
        objs.append(_arrow(ax, mxy, direction, **kwargs))
    return objs

def _lines(ax, lines, **kwargs):
    '''show the lines.'''
    objs = []
    for ls, line in lines:
        objs.extend(_line(ax, ls, line, **kwargs))
    return objs

def _arrow(ax, mxy, direction, head_width, head_length, lw, zorder, color):
    '''draw an arrow.'''
    head_vec = direction * head_length
    mxy = mxy - head_vec * 0.6
    dx, dy = direction
    obj = plt.arrow(*mxy, 1e-8 * dx, 1e-8 * dy,
              head_length=head_length, width=0,
              head_width=head_width, fc=color,
              length_includes_head=False, lw=lw, edgecolor=color, zorder=zorder)
    return obj

def _line(ax, ls, path, lw, color, zorder, use_path):
    '''draw a line connecting sxy and exy.'''
    objs = []
    def _plot_line(path_):
        if not use_path:
            sxy_, exy_ = path_
            objs.append(ax.plot([sxy_[0], exy_[0]], [
                               sxy_[1], exy_[1]], lw=lw, color=color,
                               zorder=zorder, ls=ls, solid_capstyle='butt'))
        else:
            obj = patches.PathPatch(path_, lw=lw, facecolor='none', edgecolor=color,
                               zorder=zorder, ls=ls)
            objs.append(obj)
            ax.add_patch(obj)
    if ls == '=':
        if not use_path:
            sxy, exy = path
            d = np.asarray(exy) - sxy
            unit_d = d / norm(d)
            perp_d = np.array([-unit_d[1], unit_d[0]])
            offset = perp_d * edge_setting['doubleline_space'] * lw
            ls = '-'
            _plot_line((sxy + offset, exy + offset))
            _plot_line((sxy - offset, exy - offset))
        else:
            raise NotImplementedError('Double line for C link not implemented!')
    else:
        if ls == '.': ls = '--'
        _plot_line(path)
    return objs


def _basicgeometry(xy, geo, size, color, edgecolor, lw, ls, zorder, angle):
    '''basic geometric handler.'''
    is_rect = geo[:9] == 'rectangle'
    if geo == 'circle':
        c = plt.Circle(xy, size, edgecolor=edgecolor, ls=ls,
                       facecolor=color, lw=lw, zorder=zorder)
    elif geo == 'square':
        xy = xy[0] - size, xy[1] - size
        c = plt.Rectangle(xy, 2 * size, 2 * size, edgecolor=edgecolor, ls=ls,
                          facecolor=color, lw=lw, zorder=zorder)
    elif geo[:8] == 'triangle':
        tri_path = np.array(
            [[-0.5 * np.sqrt(3), -0.5], [0.5 * np.sqrt(3), -0.5], [0, 1]])
        tri_path = rotate(tri_path, angle)
        c = plt.Polygon(xy=tri_path * size + xy, edgecolor=edgecolor, ls=ls,
                        facecolor=color, lw=lw, zorder=zorder)
    elif geo == 'diamond':
        dia_path = np.array([[-1, 0], [0, -1], [1, 0], [0, 1]])
        dia_path = rotate(dia_path, angle)
        c = plt.Polygon(xy=dia_path * size + xy, edgecolor=edgecolor, ls=ls,
                        facecolor=color, lw=lw, zorder=zorder)
    elif is_rect or geo == 'golden':
        remain = geo[9:]
        if geo == 'golden':
            height = size * 2
            width = height * 1.3
        else:
            width = size[0] * 2
            height = size[1] * 2
        xy_ = xy[0] - width / 2., xy[1] - height / 2.
        if remain == '-round':
            pad = 0.15*min(width, height)
            c = patches.FancyBboxPatch(xy_+np.array([pad,pad]), width-pad*2, height-pad*2, zorder=zorder,
                              edgecolor=edgecolor, facecolor=color, lw=lw, ls=ls,
                              boxstyle=patches.BoxStyle("Round", pad=pad))
        else:
            c = plt.Rectangle(xy_, width, height, edgecolor=edgecolor, ls=ls,
                              facecolor=color, lw=lw, zorder=zorder)
    elif geo == 'dot':
        c = plt.Circle(xy, 0.15 * size, edgecolor=edgecolor,
                       facecolor=edgecolor, lw=lw, zorder=zorder)
    elif geo in ['cross', 'plus', 'vbar', 'measure']:
        objs = []
        radi = size
        inner_fc = 'none'
        if geo == 'plus':
            path_list = [Path([(-radi, 0), (radi, 0)]), Path([(0, -radi), (0, radi)])]
        elif geo == 'vbar':
            path_list = [Path([(0, -radi), (0, radi)])]
        elif geo == 'measure':
            bottom, top, left, right, radi = np.array([-0.3, 0.6, -0.9, 0.9, 1.0])*size
            # the line
            # the curve
            x = np.linspace(left, right, 100)
            y = np.sqrt(radi**2 - x**2)
            path_list = [Path([(0, bottom), (right, top)]),
                        Path(list(zip(x, y - radi + 0.1)))]
        else:
            radi_ = radi / np.sqrt(2.)
            path_list = [Path([(-radi_, -radi_), (radi_, radi_)]),
                    Path([(radi_, -radi_), (-radi_, radi_)])]
        for pp in path_list:
            pp = rotate_translate_path(pp, angle, xy)
            objs.append(patches.PathPatch(pp, facecolor='none', edgecolor=edgecolor, lw=lw, zorder=zorder))
        return objs
    elif geo == '':
        c = plt.Circle(xy, 0, edgecolor='none', facecolor='none', ls=ls)
    else:
        raise ValueError('Geometry %s not defined!' % geo)
    return [c]

def basicgeometry_handler(theme_code, xy, size,  color, edgecolor, lw, ls, zorder, angle, inner_lw, inner_ec, inner_fc):
    '''basic geometry node handler.'''
    default_color, geo, inner_geo = theme_code
    if color is None:
        color = default_color
    if color is None:  # both color and default color is None
        color = 'none'
        edgecolor = 'none'

    # the size of node
    is_rect = geo[:9] == 'rectangle'
    if is_rect:
        if not hasattr(size, '__iter__'):
            size = (size,) * 2
        assert(len(size) == 2)
    else:
        assert(isinstance(size, numbers.Number))

    objs = _basicgeometry(xy, geo, size, color, edgecolor, lw, ls, zorder, angle)

    # add a geometric patch at the top of circle.
    if inner_geo != 'none':
        # get the size
        if inner_geo in ['measure', 'cross', 'vbar', 'plus']:
            inner_size = size
        else:
            inner_size = 0.7 * size
        objs += _basicgeometry(xy, inner_geo, inner_size, inner_fc, inner_ec, inner_lw, ls, zorder+1, angle)

    # for BLUE nodes, add a self-loop (Stands for Recurrent Unit)
    if color == BLUE and theme_code == 'nn.':
        loop = plt.Circle((xy[0], xy[1] + 1.2 * size), 0.5 * size,
                          edgecolor=edgecolor, facecolor=inner_fc, lw=lw, zorder=-5)
        objs.append(loop)
    return objs

def rotate_translate_path(path, angle, dxy=(0,0)):
    '''rotate path by angle'''
    affine = transforms.Affine2D()
    return path.transformed(affine.rotate(angle)).transformed(affine.translate(*dxy))
