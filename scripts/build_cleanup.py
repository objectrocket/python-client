#!/usr/bin/env python
# -*- coding: utf8 -*-
"""Cleanup build artifacts."""
import argparse
import logging
import os
import shutil
import sys
from glob import iglob

logger = logging.getLogger()


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('toplevel')
    parser.add_argument('--all', action='store_true')

    return parser.parse_args()


def rmtree(tree):
    try:
        logger.info('Removing "{}"'.format(tree))
        shutil.rmtree(tree)
        logger.info('Removed "{}"'.format(tree))
    except OSError as ex:
        logger.critical(str(ex))


def main():
    args = parse_args()
    toplevel = os.path.abspath(args.toplevel)

    build = os.path.join(toplevel, 'build')
    dist = os.path.join(toplevel, 'dist')
    egginfo = os.path.join(toplevel, iglob('*.egg-info').next() or '.egg-info')

    rmtree(build)
    rmtree(egginfo)

    if args.all:
        rmtree(dist)


if __name__ == '__main__':
    handler = logging.StreamHandler()
    logger.addHandler(handler)
    logger.setLevel(logging.INFO)

    sys.exit(main())
