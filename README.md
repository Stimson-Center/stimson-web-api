stimson-web-api backend
=======================

RESTful API for web page scraping and crawling

Table of Contents
=================

   * [stimson-web-api backend](#stimson-web-api-backend)
   * [Table of Contents](#table-of-contents)
   * [Getting Started](#getting-started)
      * [Microsoft Windows](#microsoft-windows)
      * [macOS](#macos)
      * [Start Docker service on your computer](#start-docker-service-on-your-computer)
      * [Get the source code hierarchy](#get-the-source-code-hierarchy)
   * [Make a Google Custom Search Engine](#make-a-google-custom-search-engine)
   * [Make a Google Cloud Console "Project" to get API key](#make-a-google-cloud-console-project-to-get-api-key)
   * [Docker](#docker)
 
# Getting Started

## Microsoft Windows

[Docker for Windows download and installation](https://docs.docker.com/docker-for-windows/install/)

## macOS

Download and install [Docker Community Edition](https://www.docker.com/community-edition). if you have Homebrew-Cask, just type `brew cask install docker`.

## Start Docker service on your computer

Once you've installed Docker Community Edition, click the docker icon in Launchpad. Then start up a container:

## Get the source code hierarchy

Open up a Microsoft Command Window or a Mac Terminal Window

```bash
    cd ~
    git clone https://github.com/Stimson-Center/stimson-web-api.git
```

# Make a Google Custom Search Engine

Go to https://www.google.com/cse/

Create a custom search engine

Get search engine ID

You can test the custom search engine by directly visiting its "Public URL" which is found in "Setup" => "Details" => "Public URL"

# Make a Google Cloud Console "Project" to get API key

Go to https://console.developers.google.com/apis/dashboard

Create a project or select

Enable APIs and services

Select Custom Search API and enable it

Click "Create credentials"

Get your credentials for Custom Search API

Go to Credentials and get API key

```bash
    cd ~/stimson-web-api
    mkdir ~/.cloudshell
    touch ~/.cloudshell/no-python-warning
    touch .env
    echo GOOGLE_SECRET_API_KEY="from google procedure above"  >> .env
    echo GOOGLE_SECRET_CUSTOM_SEARCH_ID="from google procedure above"  >> .env
```

Links:

[Google Developers Console - Projects (API Key)](https://console.developers.google.com/project)

[Best practices for securely using API keys](https://developers.google.com/console/help/new/#usingkeys)

[Google Custom Search Engine Setup (search Engine ID)](https://www.google.com/cse/all)

[Google CustomSearch API v1](http://developers.google.com/apis-explorer/#p/customsearch/v1)

# Docker

See DOCKER.md for more more details

```bash
    cd ~/stimson-web-api
    ./run_docker.sh
    open http://localhost:8080
```

To debug docker container

```bash
    docker run -p 8080:8080 -it --entrypoint=/bin/bash stimson-web-api 
```

