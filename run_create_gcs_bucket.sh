#!/bin/sh

# https://cloud.google.com/appengine/docs/flexible/python/using-cloud-storage

gsutil mb gs://stimson-gcs-datascience-bucket
gsutil defacl set public-read gs://stimson-gcs-datascience-bucket
