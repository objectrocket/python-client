#!/usr/bin/env python
# -*- coding: utf8 -*-
"""Setup script for ObjectRocket Python client."""
import objectrocket
from setuptools import find_packages, setup

with open("README.rst") as f:
    readme = f.read()

with open("requirements.txt") as f:
    requires = f.read()

setup(
    author='ObjectRocket Engineering Team',
    author_email='Anthony.Dodd@ObjectRocket.com',  # TODO(Anthony): Make this email.
    description='ObjectRocket Python Client',
    include_package_data=True,
    install_requires=requires,
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
        'Topic :: Database',
    ),
)
