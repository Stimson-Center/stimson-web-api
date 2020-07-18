#!/usr/bin/env bash
set -e

gcloud -v
gcloud components install app-engine-python
gcloud components update
gcloud config set project stimson-web-curator-api
# gcloud app deploy --project=stimson-web-curator-api --stop-previous-version --promote --verbosity=debug
gcloud app deploy --project=stimson-web-curator-api --promote
gcloud app describe --project=stimson-web-curator-api
gcloud app browse
gcloud app logs tail -s default
