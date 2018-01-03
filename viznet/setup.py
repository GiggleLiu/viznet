'''
Set up file for matrix product state.
'''


def configuration(parent_package='', top_path=None):
    from numpy.distutils.misc_util import Configuration
    config = Configuration('viznet', parent_package, top_path)
    return config
