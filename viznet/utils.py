import numpy as np
import pdb

from scipy.interpolate import interp1d

__all__ = ['rotate']


def rotate(vec, theta):
    '''
    rotate a 2D vector.

    Args:
        vec (1darray): the 2D vector.
        theta (float): the angle for rotation.

    Returns:
        1darray: the rotated vector.
    '''
    mat = np.array([[np.cos(theta), -np.sin(theta)],
                    [np.sin(theta), np.cos(theta)]])
    return mat.dot(np.transpose(vec)).T


def intersection(line, theta, align):
    '''
    get the intersection point from direction specified by theta.

    Args:
        line (2darray): an array of points.
        theta (float): direction of the intersection line.
        align (len-2 tuple): align to this point in the free dimension.

    Returns:
        tuple: the nearest intersection point.
    '''
    # rotate to y-axis
    rotated_line = rotate(line, np.pi / 2. - theta)
    rotated_xy = rotate(align, np.pi / 2. - theta)

    # get segments
    p_pre = rotated_line[0]
    segment = [p_pre]
    segments = []
    direction_pre = 0
    for p in rotated_line[1:]:
        direction = 1 if p[0] > p_pre[0] else -1
        if direction * direction_pre < 0:
            segments.append(segment)
            segment = [p_pre, p]
        else:
            segment.append(p)
        direction_pre = direction
        p_pre = p
    segments.append(segment)

    # intersect segments
    x = rotated_xy[0]
    ys = []
    for segment in segments:
        x_, y_ = np.array(segment).T
        f = interp1d(x_, y_)
        try:
            ys.append(f(x))
        except:
            pass

    # interpolate x
    index = np.argmin(ys)
    p = rotate([x, ys[index]], theta - np.pi / 2)
    return p
