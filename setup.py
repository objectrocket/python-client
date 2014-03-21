#!/usr/bin/env python
# -*- coding: utf8 -*-
"""Setup script for ObjectRocket Python client."""
import objectrocket
from setuptools import setup

with open("README.rst") as f:
    readme = f.read()

with open("requirements.txt") as f:
    requires = f.read()

setup(
    author='ObjectRocket engineering team.',
    author_email='Anthony@ObjectRocket.com',
    description='ObjectRocket Python client.',
    include_package_data=True,
    install_requires=requires,
    license='',
    long_description=readme,
    name='objectrocket',
    package_data={},
    package_dir={},
    packages=[],
    py_modules=['objectrocket'],
    url='',
    version=objectrocket.__version__,
    zip_safe=False,
    classifiers=(
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python',
        'Topic :: Database',
    ),
)
