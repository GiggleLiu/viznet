import numpy as np
from numpy.testing import dec, assert_, assert_raises, assert_almost_equal, assert_allclose
import matplotlib.pyplot as plt
from matplotlib import patches
from matplotlib.collections import PatchCollection
import pdb

from ..utils import intersection
from .. import shapes


def test_intersection():
    ring = [(0, 0), (0, 1), (1, 1), (1, 0)]
    line = [(-1, -1), (1, 1)]
    res = intersection(ring, line)
    pdb.set_trace()


def test_intersection():
    ring = [(0, 0), (0, 1), (1, 1), (1, 0), (0, 0)]
    theta = np.pi / 4.
    res = intersection(ring, theta, align=(-0.5, 0))
    assert_allclose(res, (0, 0.5))

def test_rounded_path():
    vertices = np.array([(0, 0), (1, 0), (1, 1), (0, 1)])
    path = shapes.rounded_path(vertices, 0.1)
    path2 = shapes.rounded_path(vertices+2, 0.1, close=True)
    pp = patches.PathPatch(path)
    pp2 = patches.PathPatch(path2)
    ax = plt.subplot(111)
    ax.add_patch(pp)
    ax.add_patch(pp2)
    plt.xlim(-1,5)
    plt.ylim(-1,5)
    plt.show()

def test_shapes():
    kwargs = {'ls':'--', 'lw':0.5, 'zorder':1, 'facecolor':'r', 'edgecolor': 'g'}
    plt.ion()
    ax = plt.subplot(111)
    shape_list = ['circle', 'golden', 'triangle', 'diamond', 'empty', 'dot', 'cross', 'measure', 'plus']
    for i, shape in enumerate(shape_list):
        func = eval('shapes.%s'%shape)
        for j in range(5):
            size_, angle_, roundness_, kwargs_ = 0.3, 0, 0, dict(kwargs)
            if j==1:
                size_ = 0.15
            if j==2:
                angle_ = np.pi/4.
            if j==3:
                angle_ = np.pi/4.
                roundness_ = 0.05
            if j==4:
                kwargs_['facecolor']='k'
            patches = func((i,-j), size_, angle_, roundness_, **kwargs_)
            for patch in patches:
                ax.add_patch(patch)
    plt.axis('equal')
    plt.axis('off')
    pdb.set_trace()

if __name__ == '__main__':
    test_shapes()
    test_intersection()
    test_rounded_path()
