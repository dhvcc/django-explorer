#!/bin/bash

poetry build

cd demo_app
poetry shell
pip install ../dist/django_explorer-0.1.0-py3-none-any.whl --force-reinstall
./manage.py runserver
