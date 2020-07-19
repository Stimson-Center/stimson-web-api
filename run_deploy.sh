#!/usr/bin/env bash
set -e

gcloud -v
gcloud components install app-engine-python
gcloud components update
gcloud config set project stimson-web-api
# gcloud app deploy --project=stimson-web-api --stop-previous-version --promote --verbosity=debug
gcloud app deploy --project=stimson-web-api --promote
gcloud app describe --project=stimson-web-api
gcloud app browse
gcloud app logs tail -s default
