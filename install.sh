#!/usr/bin/env bash

virtualenv $(dirname $0)/../venv --python=python3

$(dirname $0)/deploy.sh