import numpy as np
from numpy.testing import dec, assert_, assert_raises, assert_almost_equal, assert_allclose

from ..utils import intersection

def test_intersection():
    ring = [(0, 0), (0, 1), (1, 1), (1, 0)]
    line = [(-1, -1), (1, 1)]
    res = intersection(ring, line)
    pdb.set_trace()

def test_intersection():
    ring = [(0, 0), (0, 1), (1, 1), (1, 0), (0,0)]
    theta = np.pi/4.
    res = intersection(ring, theta, align=(-0.5, 0))
    print(res)
    assert_allclose(res, (0,0.5))

if __name__ == '__main__':
    test_intersection()
