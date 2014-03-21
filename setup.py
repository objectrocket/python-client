#!/usr/bin/env python
# -*- coding: utf8 -*-
"""Setup script for ObjectRocket Python client."""
import objectrocket
import setuptools.setup as setup

with open("README.rst") as f:
    readme = f.read()

with open("requirements.txt") as f:
    requires = f.read()

setup(
    name='objectrocket',
    version=objectrocket.__version__,
    description='ObjectRocket Python client.',
    long_description=readme,
    author='ObjectRocket engineering team.',
    author_email='Anthony@ObjectRocket.com',
    url='',
    packages=[],
    package_data={},
    package_dir={},
    include_package_data=True,
    install_requires=requires,
    license='',
    zip_safe=False,
    classifiers=(
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved',
        'Natural Language :: English',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python',
        'Topic :: Database',
    ),
)
