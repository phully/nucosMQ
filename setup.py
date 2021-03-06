#!/usr/bin/env python
from __future__ import print_function

import os
import sys

#from distutils.core import setup
from setuptools import setup, find_packages

import unittest

name = "nucosMQ"

#action should be one of update/minor/major
possible_action = ["major","minor","update", "no-update"]
action = "update"

if not sys.argv[1] == "sdist":
    action = "no-update"    

def my_test_suite():
    test_loader = unittest.TestLoader()
    test_suite = test_loader.discover(os.path.join(name,'test'), pattern='test*.py')
    return test_suite

rootdir = os.path.abspath(os.path.dirname(__file__))

# Restructured text project description read from file
try:
    from pypandoc import convert
    read_md = lambda f: convert(f, 'rst')
except ImportError:
    print("warning: pypandoc module not found, could not convert Markdown to RST")
    read_md = lambda f: open(f, 'r').read()

long_description = read_md('README.md')     #open(os.path.join(rootdir, 'README.md')).read()

# Python 2.7 or later needed
if sys.version_info < (2, 7, 0, 'final', 0):
    raise SystemExit('Python 2.7 or later is required!')

# Build a list of all project modules
packages = []
for dirname, dirnames, filenames in os.walk(name):
        if '__init__.py' in filenames:
            packages.append(dirname.replace('/', '.'))

package_dir = {name: name}

# Data files used e.g. in tests
package_data = {} #{name: [os.path.join(name, 'tests', 'prt.txt')]}

# The current version number - MSI accepts only version X.X.X
exec(open(os.path.join(name, 'version.py')).read())

#update the version count according to action
if action not in possible_action:
    raise SystemExit("action should be one of minor/major/update/hand")

if not action == "no-update":
    version_i = [int(x) for x in version.split(".")]
    version_i[possible_action.index(action)] += 1
    version = ".".join([str(x) for x in version_i])

    

    with open(os.path.join(name, 'version.py'), 'w') as f:
        f.write("version='"+version+"'")

print("Version:", version)

# Scripts
scripts = []
for dirname, dirnames, filenames in os.walk('scripts'):
    for filename in filenames:
        if not filename.endswith('.bat'):
            scripts.append(os.path.join(dirname, filename))

# Provide bat executables in the tarball (always for Win)
if 'sdist' in sys.argv or os.name in ['ce', 'nt']:
    for s in scripts[:]:
        scripts.append(s + '.bat')

# Data_files (e.g. doc) needs (directory, files-in-this-directory) tuples
data_files = []
for dirname, dirnames, filenames in os.walk('doc'):
        fileslist = []
        for filename in filenames:
            fullname = os.path.join(dirname, filename)
            fileslist.append(fullname)
        data_files.append(('share/' + name + '/' + dirname, fileslist))

setup(name=name,
      version=version,  # PEP440
      description='nucosMQ - a pure python message module',
      long_description=long_description,
      url='https://github.com/DocBO/nucosMQ',
      download_url = 'https://github.com/DocBO/nucosMQ/tarball/0.0.1',
      author='Oliver Braun',
      author_email='oliver.braun@nucos.de',
      license='MIT',
      # https://pypi.python.org/pypi?%3Aaction=list_classifiers
      classifiers=[
          'Development Status :: 1 - Planning',
          'Environment :: Console',
          'License :: OSI Approved :: MIT License',
          'Natural Language :: English',
          'Operating System :: OS Independent',
          'Programming Language :: Python :: 2',
          'Programming Language :: Python :: 2.7',
          'Programming Language :: Python :: 3',
          'Programming Language :: Python :: 3.4',
          'Programming Language :: Python :: 3.5',
      ],
      keywords='message queue zeroMQ snakeMQ',
      packages=packages,
      package_dir=package_dir,
      package_data=package_data,
      scripts=scripts,
      data_files=data_files,
      test_suite='setup.my_test_suite', 
      #install_requires=['distribute'],
      #install_requires=['xmlrunner'],

      )
