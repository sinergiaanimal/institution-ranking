#!/usr/bin/env bash

git pull

source ./venv.sh

# Building front-end assets
npm install
npm run build

# Updating back-end application
pip install -r requirements.txt
python manage.py migrate
python manage.py collectstatic --noinput

# Executing additional local_deploy.sh script if present
LOCAL_DEPLOY=$(dirname $0)/local_deploy.sh
if test -f "$LOCAL_DEPLOY"; then
    $LOCAL_DEPLOY
fi
