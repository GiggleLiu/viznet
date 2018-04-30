'''predefined patches.'''

from matplotlib import patches, transforms
from matplotlib.path import Path
import matplotlib.pyplot as plt
from functools import reduce
import numpy as np
import pdb
from numpy.linalg import norm

from .utils import rotate
from .setting import node_setting

_basic_prop_list =  ['ls', 'facecolor', 'edgecolor', 'lw', 'zorder']

def affine(pp, offset=(0,0), scale=1, angle=0):
    '''rotate path/patch by angle'''
    if isinstance(pp, (np.ndarray, list, tuple)):
        return rotate(pp, angle)*scale + offset
    
    # define the transformation
    _affine = transforms.Affine2D()
    if angle!=0: _affine.rotate(angle)
    if scale!=1: _affine.scale(scale)
    if not np.allclose(offset, 0): _affine.translate(*offset)

    if hasattr(pp, 'vertices'):
        # for path
        pp = pp.transformed(_affine)
    else:
        # for patch
        pp.set_transform(_affine+plt.gca().transData)
    return pp

def rounded_path(vertices, roundness, close=False):
    '''make rounded path from vertices.'''
    vertices = np.asarray(vertices)
    if roundness == 0:
        return Path(vertices if not close else np.concatenate([vertices, vertices[:1]],axis=0))
    if close:
        vertices = np.concatenate([vertices, vertices[:2]], axis=0)

    codes = [Path.MOVETO]
    vertices_new = [vertices[0]]
    if close:
        cur, nex = vertices[:2]
        vertices_new[0] = cur + (nex - cur)/norm(cur-nex)*roundness
    for pre, cur, nex in zip(vertices[:-2], vertices[1:-1], vertices[2:]):
        codes.extend([Path.LINETO, Path.CURVE3, Path.CURVE3])
        dv_pre = (pre - cur)/norm(cur-pre)*roundness
        dv_nex = (nex - cur)/norm(cur-nex)*roundness
        vertices_new.extend([cur+dv_pre,cur,cur+dv_nex])
    if not close:
        codes.append(Path.LINETO)
        vertices_new.append(vertices[-1])
    return Path(vertices_new, codes)

def _fix(d):
    '''get universal parameters for patches.'''
    nd = dict(node_setting)
    nd.update(d)
    return {k:d.get(k) for k in _basic_prop_list}

def empty(xy, *args, **kwargs):
    c = patches.Circle(xy, 0, edgecolor='none', facecolor='none')
    return [c]

def circle(xy, size, angle=None, roundness=0, args=(), **kwargs):
    c = patches.Circle(xy, size, *args, **_fix(kwargs))
    return [c]

def lines(xy, size, angle, roundness, args, **kwargs):
    vertices_list, = args
    kwargs['facecolor'] = 'none'
    objs = []
    for vertices in np.asarray(vertices_list):
        pp = rounded_path(affine(vertices, xy, size, angle), roundness, close=False)
        objs.append(patches.PathPatch(pp, **_fix(kwargs)))
    return objs

def polygon(xy, size, angle, roundness, args, **kwargs):
    vertices, = args
    path = rounded_path(affine(np.asarray(vertices), xy, size, angle), roundness=roundness, close=True)
    c = patches.PathPatch(path, **_fix(kwargs))
    return [c]

def rectangle(xy, size, angle, roundness, **kwargs):
    '''width is relative width with respect to height.'''
    if np.ndim(size) == 0:
        size = (size, size)
    width, height = 2*size[0], 2*size[1]
    xy_ = xy[0] - width / 2., xy[1] - height / 2.
    if roundness!=0:
        pad = roundness
        c = patches.FancyBboxPatch(xy_+np.array([pad,pad]), width-pad*2, height-pad*2,
                          boxstyle=patches.BoxStyle("Round", pad=pad), **_fix(kwargs))
    else:
        c = patches.Rectangle(xy_, width, height, **_fix(kwargs))
    return [c]

##########################  Derived types  #############################

def triangle(xy, size, angle, roundness, args=(), **kwargs):
    path = [[-0.5 * np.sqrt(3), -0.5], [0.5 * np.sqrt(3), -0.5], [0, 1]]
    return polygon(xy, size, angle, roundness, args=(path,), **kwargs)

def diamond(xy, size, angle, roundness, args=(), **kwargs):
    path = np.array([[-1, 0], [0, -1], [1, 0], [0, 1]])
    return polygon(xy, size, angle, roundness, args=(path,), **kwargs)

square = lambda xy, size, *args, **kwargs: rectangle(xy, (size, size), *args, **kwargs)
golden = lambda xy, size, *args, **kwargs: rectangle(xy, (1.3* size, size), *args, **kwargs)

def dot(xy, size, *args, **kwargs):
    kwargs['facecolor'] = kwargs['edgecolor']
    return circle(xy, 0.15*size, *args, **kwargs)

def cross(xy, size, angle, roundness, args=(), **kwargs):
    radi = 1.0
    radi_ = radi / np.sqrt(2.)
    path_list = [[(-radi_, -radi_), (radi_, radi_)],
            [(radi_, -radi_), (-radi_, radi_)]]
    return lines(xy, size, angle, roundness, args=(path_list,), **kwargs)

def plus(xy, size, angle, roundness, args=(), **kwargs):
    radi = 1.0
    path_list = [[(-radi, 0), (radi, 0)], [(0, -radi), (0, radi)]]
    return lines(xy, size, angle, roundness, args=(path_list,), **kwargs)

def vbar(xy, size, angle, roundness, args=(), **kwargs):
    radi = 1.0
    path_list = [[(0, -radi), (0, radi)]]
    return lines(xy, size, angle, roundness, args=(path_list,), **kwargs)

def measure(xy, size, angle, roundness, args=(), **kwargs):
    bottom, top, left, right, radi = np.array([-0.3, 0.6, -0.9, 0.9, 1.0])
    x = np.linspace(left, right, 100)
    y = np.sqrt(radi**2 - x**2)
    path_list = [[(0, bottom), (right, top)],
                list(zip(x, y - radi + 0.1))]
    return lines(xy, size, angle, roundness, args=(path_list,), **kwargs)
