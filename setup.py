#!/usr/bin/env python

from __future__ import with_statement
import distutils.core
import os
import sys

specific_install_requires = []

if sys.version_info < (2, 7):
    specific_install_requires.append('ordereddict')

# Importing setuptools adds some features like "setup.py develop", but
# it's optional so swallow the error if it's not there.
try:
    import setuptools
except ImportError:
    pass

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

tests_require = ['nose', 'rednose']

distutils.core.setup(name='StartAppSync',
      version="0.0.5",
      description="""
      StartAppSync will sync your code with your cloud environment on the StartApp Cloud.
      You can develop your cloud apps locally with editors and tools you love without any need to
      install php, ruby, node, python, mysql or mongodb on your computer :)
      """,
      author='Marian Ignev',
      author_email='m@ignev.net',
      url='http://github.com/mignev/startappsync',
      packages=['startappsync'],
      long_description=read('README.md'),
      package_dir={"startappsync":"startappsync"},

      tests_require = tests_require,
      extras_require={'test': tests_require},

      install_requires = [
      'docopt',
      'watchdog',
      'pathtools',
      'termcolor',
      ] + specific_install_requires,
      scripts= ["bin/startappsync"],
      classifiers=[
          'Development Status :: 4 - Beta',
          'Operating System :: POSIX',
          'Operating System :: POSIX :: BSD',
          'Operating System :: POSIX :: Linux',
          'Operating System :: Unix',
          'Programming Language :: Python',
          'Programming Language :: Python :: 2',
          'Programming Language :: Python :: 2.7',
          'Topic :: System :: Shells',
          'Topic :: Utilities'],
     )
