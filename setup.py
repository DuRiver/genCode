#!/bin/env/python
# filename:setup.py

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

config = {
    'description': 'Generate Code',
    'author': 'River',
    'url': 'URL to get it at.',
    'download_url': 'Where to download it.',
    'author_email': 'd.cj@outlook.com',
    'version': 'o.1',
    'install_requires': ['windll'],
    'packages': ['GenCode'],
    'scripts': [],
    'name': 'GenCode'
}

setup(**config)
