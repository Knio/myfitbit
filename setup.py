# pylint: disable=bad-whitespace

from setuptools import setup

import imp
_version = imp.load_source("myfitbit._version", "myfitbit/_version.py")

long_description = open('README.md').read()

# PyPI only supports (an old version of?) ReST.
# Doesn't seem to be compatable with Pandoc. Shame on you.

# try:
#   import pypandoc
#   long_description = pypandoc.convert(
#     long_description, 'rst', format='markdown_github')
#   with open('README.rst', 'w') as f:
#     f.write(long_description)
# except:
#   import traceback
#   traceback.print_exc()


setup(
  name    = 'myfitbit',
  version = _version.__version__,
  author  = 'Tom Flanagan',
  author_email = 'tom@zkpq.ca',
  license = 'LICENSE.txt',
  url     = 'http://github.com/Knio/myfitbit/',

  description      = 'myfitbit - ',
  long_description = long_description,
  keywords         = 'framework templating template html xhtml python html5',

  classifiers = [
    'Intended Audience :: Developers',
    'License :: OSI Approved :: GNU Lesser General Public License v3 (LGPLv3)',
    'Operating System :: OS Independent',
    'Programming Language :: Python',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.3',
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: Implementation :: PyPy',
    'Topic :: Internet :: WWW/HTTP',
    'Topic :: Software Development :: Libraries :: Python Modules',
  ],

  packages = ['myfitbit'],
  include_package_data = True,

  install_requires = [
    'requests',
    'beautifulsoup4',
  ],
)
