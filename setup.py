#-*- coding: utf-8 -*-

"""
    crxmake
    ~~~~~~~

    Setup
    `````
    $ sudo apt-get install swig # dep for m2crypto
    $ sudo pip install .
"""

from distutils.core import setup
import os

setup(
    name='crxmake',
    version='0.0.2',
    url='http://github.com/bellbind/crxmake',
    author='bellbind',
    author_email='bellbind@gmail.com',
    packages=[
        'crxmake',
        ],
    platforms='any',
    license='LICENSE',
    install_requires=[
        'm2crypto'
    ],
    scripts=[
        "scripts/crxmake"
        ],
    description="crxmake packages chrome extensions as .crx from python",
    long_description=open(os.path.join(os.path.dirname(__file__), 'README.md')).read(),
)
