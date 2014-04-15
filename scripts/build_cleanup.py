#!/usr/bin/env python
# -*- coding: utf8 -*-
"""Cleanup build artifacts."""
import argparse
import logging
import os
import shutil
import sys

logger = logging.getLogger()


class BuildCleanup(object):
    def __init__(self):
        self.parse_args()
        self.toplevel = os.path.abspath(self.args.toplevel)

        self.build = os.path.join(self.toplevel, 'build')
        self.dist = os.path.join(self.toplevel, 'dist')
        self.egginfo = os.path.join(self.toplevel, 'objectrocket.egg-info')

    def main(self):
        self.rmtree(self.build)
        self.rmtree(self.egginfo)

        if self.args.all:
            self.rmtree(self.dist)

        return 0

    def parse_args(self):
        parser = argparse.ArgumentParser()
        parser.add_argument('toplevel')
        parser.add_argument('--all', action='store_true')

        self.args = parser.parse_args()

    def rmtree(self, tree):
        try:
            shutil.rmtree(tree)
        except OSError as ex:
            logger.critical(str(ex))

if __name__ == '__main__':
    handler = logging.StreamHandler()
    logger.addHandler(handler)
    logger.setLevel(logging.INFO)

    sys.exit(BuildCleanup().main())
