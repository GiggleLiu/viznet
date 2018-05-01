import pdb
import numbers
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import patches, transforms
from matplotlib.path import Path
from numpy.linalg import norm

from .edgenode import Edge, Node, Pin, _node
from .theme import NODE_THEME_DICT, BLUE
from .utils import rotate
from .setting import node_setting, edge_setting
from .import shapes

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
        size ('huge'|'large'|'normal'|'small'|'tiny'|'dot'|tuple|float): size of node.
    '''
    setting = node_setting

    size_dict = {
        'huge': 0.9,
        'large': 0.39,
        'normal': 0.3,
        'small': 0.21,
        'tiny': 0.09,
        'dot': 0.05,
    }

    def __init__(self, style, ax=None, color=None, size='normal', roundness=0, zorder=0, rotate=0., ls='-', props=None):
        self.style = style
        self.size = size
        self.ax = ax
        self.color = color
        self.zorder = zorder
        self.rotate = rotate
        self.ls = ls
        self.node_handler = basicgeometry_handler
        self.props = props if props is not None else {}
        self.roundness = roundness

    @property
    def is_rectangular(self):
        return self._style[1] in ['rectangle']

    @property
    def _size(self):
        if isinstance(self.size, str):
            size = self.size_dict[self.size]
        else:
            size = self.size
        if self.is_rectangular and np.ndim(size)==0:
            size = [size, size]
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
        # override color
        if self.color is not None:
            color = self.color

        theme_code = self._style

        # get the size and position
        size = self._size
        if np.ndim(size) == 1 and len(size) == 2:
            xstart, xstop = self._get_range(xy[0])
            ystart, ystop = self._get_range(xy[1])
            size = (size[0] + abs(xstop - xstart)/2., size[1] + abs(ystop - ystart)/2.)
            xy = (xstop + xstart)/2., (ystart + ystop)/2.

        objs = self.node_handler(theme_code, xy, size, self.roundness, facecolor=self.color,
                ls=self.ls, zorder=self.zorder, angle=self.rotate, props=self.props)

        # add patches
        for p in objs:
            ax.add_patch(p)
            #shapes.affine(p, offset=xy, scale=np.atleast_1d(self._size)[0], angle=self.rotate)
        node = Node(objs, xy, self)
        return node

    @property
    def _style(self):
        if isinstance(self.style, str):
            return NODE_THEME_DICT[self.style]
        else:
            return self.style

    def _get_range(self, x):
        if isinstance(x, slice):   # gridwise operation.
            if not self.is_rectangular:
                raise ValueError('Only Rectangular support slice plot!')
            return x.start, x.stop
        else:
            return x, x

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
        start, end = _node(startend[0]), _node(startend[1])
        sxy, exy = np.asarray(start.position), np.asarray(end.position)
        d = exy - sxy
        unit_d = d / norm(d)
        sxy = start.get_connection_point(unit_d)
        exy = end.get_connection_point(-unit_d)

        arrows, lines = self.line_handler(sxy, exy, self.style, head_length)
        objs = _arrows(ax, arrows, head_width=head_width, head_length=head_length, lw=lw, zorder=self.zorder, color=self.color)
        objs += _lines(ax, lines, lw=lw, color=self.color, zorder=self.zorder, use_path=False)
        return Edge(objs, sxy, exy, start, end, brush=self)

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
        start, end = _node(startend[0]), _node(startend[1])
        sxy, exy = np.asarray(start.position), np.asarray(end.position)
        
        arrows, lines, (sxy_, exy_) = self.line_handler(sxy, exy, self.style, self.offsets, self.roundness, head_length)
        objs = _arrows(ax, arrows, head_width=head_width, head_length=head_length, lw=lw, zorder=self.zorder, color=self.color)
        objs += _lines(ax, lines, lw=lw, color=self.color, zorder=self.zorder, use_path=True)
        return Edge(objs, sxy_, exy_, start, end, brush=self)

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
            objs.extend(ax.plot([sxy_[0], exy_[0]], [
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

def _basicgeometry(xy, geo, size, angle, roundness, props, **kwargs):
    '''basic geometric handler.'''
    return eval('shapes.%s'%geo)(xy, size, angle, roundness, props=props, **kwargs)

def basicgeometry_handler(theme_code, xy, size, roundness, facecolor, ls, zorder, angle, props):
    '''basic geometry node handler.'''
    default_color, geo, inner_geo = theme_code
    edgecolor = node_setting['edgecolor']
    lw = node_setting['lw']
    if facecolor is None:
        facecolor = default_color
    if facecolor is None:  # both color and default color is None
        facecolor = 'none'
        edgecolor = 'none'

    objs = _basicgeometry(xy, geo, size, angle,roundness, props, facecolor=facecolor, edgecolor=edgecolor, ls=ls, zorder=zorder, lw=lw)

    # add a geometric patch at the top of circle.
    if inner_geo != 'none':
        # get the size
        if inner_geo in ['measure', 'cross', 'vbar', 'plus']:
            inner_size = size
        else:
            inner_size = 0.7 * size

        inner_fc = node_setting['inner_facecolor']
        inner_ec = node_setting['inner_edgecolor']
        inner_lw = node_setting['inner_lw']
        objs += _basicgeometry(xy, inner_geo, inner_size, angle, roundness, props, facecolor=inner_fc, edgecolor=inner_ec, lw=inner_lw, ls=ls, zorder=zorder+1)

    # for BLUE nodes, add a self-loop (Stands for Recurrent Unit)
    if facecolor == BLUE and theme_code == 'nn.':
        loop = plt.Circle((xy[0], xy[1] + 1.2 * size), 0.5 * size,
                          edgecolor=edgecolor, facecolor=inner_fc, lw=lw, zorder=-5)
        objs.append(loop)
    return objs

def rotate_translate_path(path, angle, dxy=(0,0)):
    '''rotate path by angle'''
    affine = transforms.Affine2D()
    return path.transformed(affine.rotate(angle)).transformed(affine.translate(*dxy))
