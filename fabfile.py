#!/usr/bin/env python
# -*- coding: utf8 -*-
"""Python client fabric commands.

This is intended to be run from mon1.
"""
import logging

from fabric.api import env, execute, lcd, local, roles
from fabric.contrib.project import rsync_project
from fabric.tasks import Task

# Logging configuration.
logger = logging.getLogger()
handler = logging.StreamHandler()
logger.addHandler(handler)
logger.setLevel(logging.INFO)

env.roledefs = {
    'app_servers': ['app{}.sjc.objectrocket.com'.format(x) for x in range(4)],
}


class RollDocs(Task):
    """Build and deploy the client documentation."""
    name = 'roll_docs'

    def _build_docs(self):
        """Build the client documentation."""
        with lcd('/root/rollout/python-client'):
            # Equivalent to ``python setup.py build_sphinx -E``.
            local('source /root/.virtualenvs/python-client/bin/activate && tox -e docs -- -E')

    def _clean_repo(self):
        """Clean the repo after the tox runs."""
        with lcd('/root/rollout/python-client/'):
            local('git clean -fdx')

    @roles('app_servers')
    def _deploy_docs(self):
        """Deploy the client documentation."""
        with lcd('/root/rollout/python-client/docs/build/html/'):
            rsync_project(remote_dir='/docs/clients/python/', local_dir='./',
                          delete=True, exclude='.git')

    def _update_repo(self):
        """Update the git repository."""
        with lcd('/root/rollout/python-client/'):
            local('git pull')

    def run(self):
        logger.info('Rolling the python client documentation.')
        self._clean_repo()
        self._update_repo()
        self._build_docs()
        execute(self._deploy_docs)
        self._clean_repo()

roll_docs = RollDocs()
