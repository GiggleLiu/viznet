'''
node class.
'''

import pdb
import numpy as np
import matplotlib.pyplot as plt

from .setting import annotate_setting

__all__ = ['Edge', 'Node']


class EdgeNode(object):
    def text(self, text, position='center', fontsize=None, color='k', text_offset=None):
        '''
        Args:
            position: position of text, use string 'center'|'left'|'right'|'top','bottom' to specify direction.
            fontsize (int/None): override default fontsize.
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
    Attributes:
        style (tuple): style.
        obj(Patch): matplotlib patch object.
    '''

    def __init__(self, obj, style, ax):
        self.style = style
        self.obj = obj
        self.ax = ax

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
        get a pin in specific direction.
        '''
        offset_dict = self._offset_dict
        loc = offset_dict[direction] + self.position
        if align is not None:
            target = align.position
            if direction in ['bottom', 'top']:
                loc[0] = target[0]
            else:
                loc[1] = target[1]
        return Pin(loc)

    @property
    def position(self):
        shape = self.style[1]
        if isinstance(self.obj, plt.Circle):
            return np.array(self.obj.center)
        elif isinstance(self.obj, plt.Rectangle):
            x, y = self.obj.get_xy()
            return np.array([x + self.obj.get_width() / 2., y + self.obj.get_height() / 2.])
        elif isinstance(self.obj, plt.Polygon):
            return self.obj.get_path().vertices[:-1].mean(axis=0)
        else:
            raise

    @property
    def height(self):
        shape = self.style[1]
        if isinstance(self.obj, plt.Circle):
            return self.obj.radius * 2
        elif isinstance(self.obj, plt.Rectangle):
            return self.obj.get_height()
        elif isinstance(self.obj, plt.Polygon):
            ys = self.obj.get_path().vertices[:-1, 1]
            return abs(ys - ys.mean()).max() * 2
        else:
            raise

    @property
    def width(self):
        shape = self.style[1]
        if isinstance(self.obj, plt.Circle):
            return self.obj.radius * 2
        elif isinstance(self.obj, plt.Rectangle):
            return self.obj.get_width()
        elif isinstance(self.obj, plt.Polygon):
            xs = self.obj.get_path().vertices[:-1, 0]
            return abs(xs - xs.mean()).max() * 2
        else:
            raise

    def get_connection_point(self, direction):
        '''
        Args:
            direction (1darray): unit vector pointing to target direction.
        '''
        shape = self.style[1]
        if shape == 'circle':
            return self.obj.center + self.obj.radius * direction
        else:
            if shape == 'square' or shape == 'rectangle':
                x, y = self.obj.get_xy()
                w, h = self.obj.get_width(), self.obj.get_height()
                vertices = np.array(
                    [(x, y), (x + w, y), (x + w, y + h), (x, y + h), (x, y)])
            else:
                vertices = candidates = self.obj.get_path().vertices
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
    Attributes:
        style (tuple): style.
        obj(Patch): matplotlib patch object.
    '''

    def __init__(self, obj, start_xy, end_xy, start, end, ax):
        self.obj = obj
        self.start = start
        self.end = end
        self.start_xy = start_xy
        self.end_xy = end_xy
        self.ax = ax

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


class Pin(EdgeNode):
    def __init__(self, position):
        self.position = position

    @property
    def width(self):
        return 0.

    @property
    def height(self):
        return 0.

    def get_connection_point(self, *arg, **kwargs):
        return self.position
