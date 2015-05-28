#!/usr/bin/env python
# -*- coding: utf8 -*-
"""Setup script for ObjectRocket Python client."""
import objectrocket
from setuptools import find_packages, setup

with open('README.md') as f:
    readme = f.read()

with open('requirements/prod.txt') as f:
    requirements = f.read()

setup(
    author='ObjectRocket Engineering Team',
    author_email='anthony.dodd@rackspace.com',
    description='ObjectRocket Python Client',
    include_package_data=True,
    install_requires=requirements,
    long_description=readme,
    name='objectrocket',
    packages=find_packages(exclude=['tests*']),
    version=objectrocket.__version__,
    zip_safe=False,
    classifiers=(
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2.7',
        'Topic :: Database'
    )
)
