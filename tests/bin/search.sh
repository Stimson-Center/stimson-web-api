#!/usr/bin/env bash

curl -H "Content-Type: application/json" -X POST -d '{"allOfTheseWords": "IUU", "orTerms": null, "exactTerms": null, "fileType": null, "language": "any", "excludeTerms": null, "lowRange": null, "highRange": null, "country": "any", "start": 1, "siteSearch": null, "termsAppearing": null, "sort": null}' https://stimson-web-api.uk.r.appspot.com/search
