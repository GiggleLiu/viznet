'''
node class.
'''

import numpy as np

setting = {
        'fontsize': 12,
        }

__all__ = ['Edge', 'Node']

class EdgeNode(object):
    def text(self, text, position='center', fontsize = None, color='k', text_offset=0.1):
        '''
        Args:
            position: position of text, use string 'center'|'left'|'right'|'top','bottom' to specify direction.
            fontsize (int/None): override default fontsize.
        '''
        if fontsize is None:
            fontsize = setting['fontsize']
        va = ha = 'center'

        if isinstance(position, str):
            width, height = self.width, self.height
            if position == 'center':
                position = self.position
            elif position == 'right':
                position = self.position + np.array([width*0.5+text_offset, 0])
                ha = 'left'
            elif position == 'left':
                position = self.position + np.array([-width*0.5-text_offset, 0])
                ha = 'right'
            elif position == 'top':
                position = self.position + np.array([0, height*0.5+text_offset])
                va = 'bottom'
            elif position == 'bottom':
                position = self.position + np.array([0, -height*0.5-text_offset])
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
    def position(self):
        shape = self.style[1]
        if shape == 'circle':
            return np.array(self.obj.center)
        elif shape == 'square' or shape == 'rectangle':
            x, y = self.obj.get_xy()
            return np.array([x+self.obj.get_width()/2., y+self.obj.get_height()/2.])
        else:
            return self.obj.get_path().vertices[:-1].mean(axis=0)

    @property
    def height(self):
        shape = self.style[1]
        if shape == 'circle':
            return self.obj.radius*2
        else:
            ys = self.obj.get_path().vertices[:-1,1]
            return  abs(ys - ys.mean()).max()*2

    def get_connection_point(self, direction):
        '''
        Args:
            direction (1darray): unit vector pointing to target direction.
        '''
        shape = self.style[1]
        if shape == 'circle':
            return self.obj.center+self.obj.radius*direction
        else:
            if shape == 'square' or shape == 'rectangle':
                x, y = self.obj.get_xy()
                w, h = self.obj.get_width(), self.obj.get_height()
                vertices = np.array([(x,y), (x+w, y), (x+w, y+h), (x, y+h), (x,y)])
            else:
                vertices = candidates = self.obj.get_path().vertices
            # only allowed to connect edge center or vertex.
            edge_centers = (vertices[:-1]+vertices[1:])/2.
            candidates = np.concatenate([vertices[:-1], edge_centers], axis=0)

            vdirection = [-direction[1], direction[0]]
            candidates_ = candidates- self.position
            distance = candidates_.dot(direction)-abs(candidates_.dot(vdirection))
            return candidates[np.argmax(distance)]

    @property
    def width(self):
        shape = self.style[1]
        if shape == 'circle':
            return self.obj.radius*2
        else:
            xs = self.obj.get_path().vertices[:-1,0]
            return  abs(xs - xs.mean()).max()*2


class Edge(EdgeNode):
    '''
    Attributes:
        style (tuple): style.
        obj(Patch): matplotlib patch object.
    '''
    def __init__(self, obj, start, end, ax):
        self.obj = obj
        self.start = start
        self.end = end
        self.ax = ax

    @property
    def position(self):
        return (self.start.position+self.end.position)/2.

    @property
    def width(self):
        return 0.

    @property
    def height(self):
        return 0.
