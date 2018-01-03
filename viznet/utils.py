import numpy as np

__all__ = ['rotate']


def rotate(vec, theta):
    '''Rotate leg.'''
    mat = np.array([[np.cos(theta), -np.sin(theta)],
                    [np.sin(theta), np.cos(theta)]])
    return mat.dot(np.transpose(vec)).T
