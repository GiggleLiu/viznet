#!/usr/bin/env python
import os
import sys

descr = """Python module for network visualization."""

DISTNAME = 'viznet'
DESCRIPTION = descr
with open(os.path.join(os.path.dirname(__file__), 'README.md')) as f:
    LONG_DESCRIPTION = f.read()
MAINTAINER = 'Giggle Liu',
MAINTAINER_EMAIL = 'cacate0129@gmail.com',
URL = 'https://gitlab.theory.iphy.ac.cn/codes/viznet'
LICENSE = 'MIT'
DOWNLOAD_URL = URL
PACKAGE_NAME = 'viznet'
EXTRA_INFO = dict(
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: MIT',
        'Topic :: Scientific/Engineering',
        'Topic :: Software Development',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: POSIX',
        'Operating System :: Unix',
        'Operating System :: MacOS',
        'Programming Language :: Fortran',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
    ]
)

try:
    import setuptools  # If you want to enable 'python setup.py develop'
    EXTRA_INFO.update(dict(
        zip_safe=False,   # the package can run out of an .egg file
        include_package_data=True,
    ))
except:
    print('setuptools module not found.')
    print("Install setuptools if you want to enable \
'python setup.py develop'.")


def configuration(parent_package='', top_path=None, package_name=DISTNAME):
    if os.path.exists('MANIFEST'):
        os.remove('MANIFEST')

    from numpy.distutils.misc_util import Configuration
    config = Configuration(None, parent_package, top_path)

    # Avoid non-useful msg: "Ignoring attempt to set 'name' (from ... "
    config.set_options(
        ignore_setup_xxx_py=True,
        assume_default_configuration=True,
        delegate_options_to_subpackages=True,
        quiet=True
    )

    config.add_subpackage(PACKAGE_NAME)
    return config


def get_version():
    """Obtain the version number"""
    import imp
    mod = imp.load_source('version', os.path.join(PACKAGE_NAME, 'version.py'))
    return mod.__version__


def setup_package():
    # Call the setup function
    metadata = dict(
        name=DISTNAME,
        maintainer=MAINTAINER,
        maintainer_email=MAINTAINER_EMAIL,
        description=DESCRIPTION,
        license=LICENSE,
        url=URL,
        download_url=DOWNLOAD_URL,
        long_description=LONG_DESCRIPTION,
        version=get_version(),
        install_requires=[
            'numpy',
            'scipy',
            'matplotlib',
        ],
        # test_suite="nose.collector",
        **EXTRA_INFO
    )

    if (len(sys.argv) >= 2 and
            ('--help' in sys.argv[1:] or sys.argv[1]
             in ('--help-commands', 'egg_info', '--version', 'clean'))):

        # For these actions, NumPy is not required.
        try:
            from setuptools import setup
        except ImportError:
            from distutils.core import setup

        metadata['version'] = get_version()
    else:
        metadata['configuration'] = configuration
        from numpy.distutils.core import setup
    setup(**metadata)


if __name__ == "__main__":
    setup_package()
