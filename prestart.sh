#! /usr/bin/env sh

echo "Running customized /app/prestart.sh:"
export GOOGLE_APPLICATION_CREDENTIALS=/app/.GOOGLE_APPLICATION_CREDENTIALS.json
export GCS_STORAGE_BUCKET: "stimson-gcs-datascience-bucket"
export NGINX_HTTP_PORT_NUMBER=8080
# export NGINX_HTTPS_PORT_NUMBER=8443

