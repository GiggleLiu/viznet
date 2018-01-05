import numpy as np

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
