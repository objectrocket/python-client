#!/usr/bin/env python
# -*- coding: utf8 -*-
"""Cleanup build artifacts."""
import argparse
import os
import shutil


class BuildCleanup(object):
    def __init__(self):
        self.parse_args()
        self.toplevel = os.path.abspath(self.args.toplevel)

        self.build = os.path.join(self.toplevel, 'build')
        self.dist = os.path.join(self.toplevel, 'dist')
        self.egginfo = os.path.join(self.toplevel, 'objectrocket.egg-info')

    def main(self):
        shutil.rmtree(self.build)
        shutil.rmtree(self.egginfo)

        if self.args.all:
            shutil.rmtree(self.dist)

    def parse_args(self):
        parser = argparse.ArgumentParser()
        parser.add_argument('toplevel')
        parser.add_argument('--all', action='store_true')

        self.args = parser.parse_args()

if __name__ == '__main__':
    BuildCleanup().main()
