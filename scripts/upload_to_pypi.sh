#!/bin/bash
[[ -z $PYPI_USERNAME ]] && echo 'Env var $PYPI_USERNAME must be defined.' && exit 1
[[ -z $PYPI_PASSWORD ]] && echo 'Env var $PYPI_PASSWORD must be defined.' && exit 1
twine upload -r $1 -u $PYPI_USERNAME -p $PYPI_PASSWORD --config-file tox.ini --skip-existing dist/*
