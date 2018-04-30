'''
node class.
'''

import pdb
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import patches

from .setting import annotate_setting
from .utils import intersection

__all__ = ['Edge', 'Node', 'Pin']


class EdgeNode(object):
    def text(self, text, position='center', fontsize=None, color='k', text_offset=None):
        '''
        text an Edge|Node|Pin.

        Args:
            text (str): the text shown.
            position ('center'|'left'|'right'|'top'|'bottom', default='center'): position of text.
            fontsize (int|None, default=None): override default fontsize.
            color (str,default='k'): color.
            text_offset (float|None,default=None): the displacement of text.

        Returns:
            matplotlib text object.
        '''
        if fontsize is None:
            fontsize = annotate_setting['fontsize']
        if text_offset is None:
            text_offset = annotate_setting['text_offset']
        va = ha = 'center'

        if isinstance(position, str):
            width, height = self.width, self.height
            if position == 'center':
                position = self.position
            elif position == 'right':
                position = self.position + \
                    np.array([width * 0.5 + text_offset, 0])
                ha = 'left'
            elif position == 'left':
                position = self.position + \
                    np.array([-width * 0.5 - text_offset, 0])
                ha = 'right'
            elif position == 'top':
                position = self.position + \
                    np.array([0, height * 0.5 + text_offset])
                va = 'bottom'
            elif position == 'bottom':
                position = self.position + \
                    np.array([0, -height * 0.5 - text_offset])
                va = 'top'
            else:
                raise
        return self.ax.text(position[0], position[1], text, va=va, ha=ha, fontsize=fontsize, color=color)


class Node(EdgeNode):
    '''
    A patch with shape and style, defines the allowed connection points, and create pins for connection.

    Attributes:
        objs(list): a list matplotlib patch object, with the first the primary object.
        brush (NodeBrush): brush.
    '''

    def __init__(self, objs, brush):
        self.brush = brush
        self.objs = objs

    @property
    def path(self):
        obj = self.obj
        trans = obj.get_transform()
        path = trans.transform_path(obj.get_path())
        if obj.axes is not None:
            path = obj.axes.transData.inverted().transform_path(path)
        return path.vertices

    @property
    def obj(self):
        '''get the primary object.'''
        return self.objs[0]

    @property
    def ax(self):
        '''get the primary object.'''
        return self.obj.axes

    @property
    def _offset_dict(self):
        w, h = self.width, self.height
        offset_dict = {
            'top': np.array([0, h / 2.]),
            'bottom': np.array([0, -h / 2.]),
            'left': np.array([-w / 2., 0]),
            'right': np.array([w / 2., 0]),
        }
        return offset_dict

    def __getattr__(self, name):
        try:
            d1, d2 = name.split('_')
            offset_dict = self._offset_dict
            offset = offset_dict[d1] + offset_dict[d2] * 0.8
            return Pin(offset + self.position)
        except:
            raise AttributeError('%s' % name)

    def pin(self, direction, align=None):
        '''
        obtain a pin on specific surface.

        Args:
            direction ('top'\|'bottom'\|'left'\|'right'\|float): specifies the surface to place a pin, or theta to specift the direction.
            align (:obj:`viznet.EdgeNode`\|tuple|None, default=None): align y-axis for 'left' and 'right' pin, x-axis for 'top' and 'bottom' pin.

        Returns:
            :obj:`viznet.Pin`: the pin for wire connection.
        '''
        if isinstance(direction, str):
            offset_dict = self._offset_dict
            loc = offset_dict[direction] + self.position
            if align is not None:
                align = _node(align)
                target = align.position
                if direction in ['bottom', 'top']:
                    loc[0] = target[0]
                elif direction in ['left', 'right']:
                    loc[1] = target[1]
                else:
                    raise
        else:
            loc = intersection(self.path, direction,
                               align=self.position if align is None else (align.position if isinstance(align, EdgeNode) else align))
        return Pin(loc)

    @property
    def position(self):
        '''center of a node'''
        shape = self.brush.style[1]
        if isinstance(self.obj, plt.Circle):
            return np.array(self.obj.center)
        elif isinstance(self.obj, (plt.Rectangle, patches.FancyBboxPatch)):
            x, y = self.obj.get_x(), self.obj.get_y()
            return np.array([x + self.obj.get_width() / 2., y + self.obj.get_height() / 2.])
        elif isinstance(self.obj, (plt.Polygon, patches.PathPatch)):
            return self.path[:-1].mean(axis=0)
        else:
            raise

    @property
    def height(self):
        shape = self.brush.style[1]
        if isinstance(self.obj, plt.Circle):
            return self.obj.radius * 2
        elif isinstance(self.obj, plt.Rectangle):
            return self.obj.get_height()
        elif isinstance(self.obj, patches.FancyBboxPatch):
            return self.obj.get_height() + 2*self.obj.get_boxstyle().pad
        elif isinstance(self.obj, (plt.Polygon, patches.PathPatch)):
            ys = self.path[:-1, 1]
            return abs(ys - ys.mean()).max() * 2
        else:
            raise

    @property
    def width(self):
        shape = self.brush.style[1]
        if isinstance(self.obj, plt.Circle):
            return self.obj.radius * 2
        elif isinstance(self.obj, plt.Rectangle):
            return self.obj.get_width()
        elif isinstance(self.obj, patches.FancyBboxPatch):
            return self.obj.get_width() + 2*self.obj.get_boxstyle().pad
        elif isinstance(self.obj, (plt.Polygon, patches.PathPatch)):
            xs = self.path[:-1, 0]
            return abs(xs - xs.mean()).max() * 2
        else:
            raise

    def get_connection_point(self, direction):
        '''
        Args:
            direction (1darray): unit vector pointing to target direction.
        '''
        shape = self.brush.style[1]
        if shape == 'circle':
            return self.obj.center + self.obj.radius * direction
        else:
            vertices = candidates = self.path
            # only allowed to connect edge center or vertex.
            edge_centers = (vertices[:-1] + vertices[1:]) / 2.
            candidates = np.concatenate([vertices[:-1], edge_centers], axis=0)

            vdirection = [-direction[1], direction[0]]
            candidates_ = candidates - self.position
            distance = candidates_.dot(
                direction) - abs(candidates_.dot(vdirection))
            return candidates[np.argmax(distance)]

    @property
    def center(self):
        return Pin(self.position)


class Edge(EdgeNode):
    '''
    An Edge connecting two `EdgeNode` instance.

    Attributes:
        obj (:obj:`Patch`): matplotlib line object.
        start_xy (tuple): start position.
        end_xy (tuple): end position.
        start (EdgeNode): start node.
        end (EdgeNode): end node.
        brush (:obj:`EdgeBrush`): brush.
    '''

    def __init__(self, objs, start_xy, end_xy, start, end, brush):
        self.objs = objs
        self.start = start
        self.end = end
        self.start_xy = np.asarray(start_xy)
        self.end_xy = np.asarray(end_xy)
        self.brush = brush

    @property
    def ax(self):
        '''get the primary object.'''
        return self.obj.axes

    @property
    def obj(self):
        return self.objs[0]

    @property
    def position(self):
        return (self.start_xy + self.end_xy) / 2.

    @property
    def width(self):
        return 0.

    @property
    def height(self):
        return 0.

    @property
    def center(self):
        return Pin(self.position)

    def head(self):
        return Pin(self.tail_xy)

    def tail(self):
        return Pin(self.start_xy)


class Pin(np.ndarray, EdgeNode):
    '''
    Simple Dot used for connecting wires.
    '''
    __array_priority__ = 0  # if it is >0, __str__ will not work.

    def __new__(subtype, param, ax=None, *args, **kwargs):
        if isinstance(param, subtype):
            obj = param
        else:
            dim = np.ndim(param)
            obj = np.asarray(param, *args, **kwargs).view(subtype)
        obj._ax = ax
        return obj

    def __array_finalize__(self, obj):
        if obj is None:
            return
        self._ax = obj._ax if hasattr(obj, '_ax') else None

    @property
    def ax(self):
        if self._ax is None:
            return plt.gca()
        return self._ax

    @property
    def width(self):
        return 0.

    @property
    def height(self):
        return 0.

    def get_connection_point(self, *arg, **kwargs):
        return tuple(self)

    @property
    def position(self):
        return tuple(self)

def _node(node):
    if not hasattr(node, 'position'):
        return Pin(node)
    else:
        return node

