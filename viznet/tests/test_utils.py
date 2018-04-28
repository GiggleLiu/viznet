import numpy as np
from numpy.testing import dec, assert_, assert_raises, assert_almost_equal, assert_allclose
import matplotlib.pyplot as plt
from matplotlib import patches

from ..utils import intersection
from ..brush import rounded_path


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
    path = rounded_path([(0, 0), (1, 0), (1, 1), (0, 1)], 0.1)
    pp = patches.PathPatch(path)
    ax = plt.subplot(111)
    ax.add_patch(pp)
    plt.xlim(-2,2)
    plt.ylim(-2,2)
    plt.show()


if __name__ == '__main__':
    test_intersection()
    test_rounded_path()
