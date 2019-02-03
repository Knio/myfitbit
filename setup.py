# pylint: disable=bad-whitespace

from setuptools import setup

import imp
_version = imp.load_source("myfitbit._version", "myfitbit/_version.py")

long_description = open('README.md').read()

setup(
  name    = 'myfitbit',
  version = _version.__version__,
  author  = 'Tom Flanagan',
  author_email = 'tom@zkpq.ca',
  license = 'LICENSE.txt',
  url     = 'http://github.com/Knio/myfitbit/',

  description      = 'export fitbit data',
  long_description = long_description,
  keywords         = 'fitbit data export json',

  classifiers = [
    'Environment :: Console',
    'Intended Audience :: Developers',
    'Intended Audience :: Healthcare Industry',
    'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
    'Operating System :: OS Independent',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.3',
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
    'Programming Language :: Python :: 3.7',
    'Programming Language :: Python :: Implementation :: PyPy',
    'Programming Language :: Python',
    'Topic :: Scientific/Engineering :: Medical Science Apps.',
    'Topic :: Scientific/Engineering :: Visualization',
    'Topic :: Software Development :: Libraries :: Python Modules',
    'Topic :: System :: Archiving',
    'Topic :: Utilities',
  ],

  packages = ['myfitbit'],
  include_package_data = True,

  install_requires = [
    'requests',
    'dominate',
  ],
)
