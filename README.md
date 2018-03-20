# Crawler

A simple crawler that classifies the links in the page.

# Installation

* Clone the repo
* Create a virtualenv with `python3 -m venv crawler-env`
* Activate the virtualenv with `source crawler-env/bin/activate`
* Run the crawler with `python run.py --url https://www.example.com --limit 1`

# Usage

usage: run.py [-h] --url URL [--limit LIMIT]

A simple web cralwer

optional arguments:
  -h, --help     show this help message and exit
  --url URL      URL to crawl
  --limit LIMIT  Number of internal URLs to crawl

# License

Copyright © 2018 Karthikeyan S

Distributed under the MIT Public License
