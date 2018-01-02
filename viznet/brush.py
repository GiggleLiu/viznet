import pdb
import numpy as np
import matplotlib.pyplot as plt

from .edgenode import Edge, Node
from .theme import NODE_THEME_DICT, BLUE

class Brush(object):
    pass

class NodeBrush(Brush):
    '''
    Attributes:
        size ('huge'|'large'|'normal'|'small'|'tiny'): size of node.
    '''
    size_dict = {
            'large':3,
            'large':1.5,
            'normal':1.0,
            'small':0.7,
            'tiny':0.3,
            }

    def __init__(self, style, ax, size='normal'):
        self.style = style
        self.size = size
        self.ax = ax

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
        '''
 
        color, geo, inner_geo, with_edge = self._style
        edgecolor = 'k' if with_edge else None
        if color is None:
            edgecolor = color = 'none'
        size = self._size

        if geo == 'circle':
            c = plt.Circle(xy, 0.2*size, edgecolor=edgecolor,
                       facecolor=color, lw=0.7, zorder=0)
        elif geo == 'square':
            a = size*0.4
            xy = xy[0]-a/2., xy[1]-a/2.
            c = plt.Rectangle(xy, a, a, edgecolor=edgecolor,
                       facecolor=color, lw=0.7, zorder=0)
        elif geo[:8] == 'triangle':
            r = size*0.2
            tri_path = np.array([[-0.5 * np.sqrt(3), -0.5], [0.5 * np.sqrt(3), -0.5], [0, 1]])
            if geo == 'triangle_r':
                tri_path = -tri_path
            c = plt.Polygon(xy= tri_path * r  + xy, edgecolor=edgecolor, facecolor=color, lw=0.7, zorder=0)
        else:
            raise
        self.ax.add_patch(c)

        # add a geometric patch at the top of circle.
        if inner_geo != 'none':
            if inner_geo == 'circle':
                g = plt.Circle(xy, 0.7 * radius, edgecolor='k',
                           facecolor='none', lw=0.7, zorder=101)
            elif inner_geo == 'triangle':
                g = plt.Polygon(xy=np.array([[-0.5 * np.sqrt(3), -0.5], [0.5 * np.sqrt(3), -0.5], [
                            0, 1]]) * 0.7 * radius + xy, edgecolor='k', facecolor='none', lw=0.7, zorder=101)
            else:
                raise ValueError('Inner Geometry %s not defined!' % geo)
            self.ax.add_patch(g)

        # for BLUE nodes, add a self-loop (Stands for Recurrent Unit)
        if color == BLUE and self.style[:3]=='nn.':
            loop = Circle((xy[0], xy[1] + 1.2 * radius), 0.5 * radius,
                          edgecolor='k', facecolor='none', lw=0.7, zorder=-5)
            self.ax.add_patch(loop)

        return Node(c, self._style, ax=self.ax)


class EdgeBrush(Brush):
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
        '''
        start, end = startend
        sxy, exy = np.array(start.position), np.array(end.position)
        d = exy - sxy
        unit_d = d / np.linalg.norm(d)
        sxy = start.get_connection_point(unit_d)
        exy = end.get_connection_point(-unit_d)
        d = exy - sxy
        lw = self.lw
        arr = self.ax.arrow(sxy[0], sxy[1], d[0], d[1],
                            head_length=0.12*lw if self.style=='arrow' else 0, width=0.015*lw,
                            head_width=8e-2*lw, fc=self.color,
                            length_includes_head=True, lw=0, edgecolor='none')
        if self.style == 'directed':
            mxy = sxy + d/2. + unit_d*0.06*lw
            plt.arrow(mxy[0], mxy[1], 0.01*d[0], 0.01*d[1],
                            head_length=0.12*lw, width=0.015*lw,
                            head_width=8e-2*lw, fc=self.color,
                            length_includes_head=True, lw=0, edgecolor='none')

        return Edge(arr, start, end, ax=self.ax)

