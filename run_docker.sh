#!/bin/sh

docker system prune --force
rm -rf backend/.venv
docker build -t stimson-web-api . 
docker run -p 8080:8080 -it stimson-web-api
