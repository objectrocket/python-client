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
    author='ObjectRocket engineering team.',
    author_email='Engineering@ObjectRocket.com',  # TODO(Anthony): Make this email.
    description='ObjectRocket Python client.',
    include_package_data=True,
    install_requires=requires,
    long_description=readme,
    name='objectrocket',
    # Gather any data files.
    # package_data={'': ['datafiles/*']},
    packages=find_packages(exclude=['tests*']),
    version=objectrocket.__version__,
    zip_safe=False,
    classifiers=(
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python',
        'Topic :: Database',
    ),
)
