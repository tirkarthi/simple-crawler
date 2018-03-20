import re
import json

import pprint
import requests
from lxml.html import document_fromstring
from urllib.parse import urlparse, urljoin


def form_url(url):
    '''
    :param: url - string - URL to check for http
    :return: url - string - Return a URL with http scheme if not present
    '''
    if not (url.startswith("http://") or url.startswith("https://")):
        url = "http://" + url

    return url

def parse_url(url):
    '''
    :param: url - string - URL to parse
    :return: parsed_url - object - Parsed URL object
    '''
    url = form_url(url)
    return urlparse(url)

def is_same_domain(url, base_url):
    '''
    :param: url - string - URL to check
    :param: base_url - string - base URL to be checked against
    :reurn: same_domain - boolean - Whether URL belongs to the same domain or not
    '''
    parsed_url = parse_url(url)
    parsed_base_url = parse_url(base_url)

    return parsed_base_url.netloc in  parsed_url.netloc

def is_resource(url):
    '''
    :param: url - string - URL to check
    :return: resource_file - boolean - Whether the URL is a file or not
    '''
    FILE_REGEX = r'\.\w+$'

    parsed_url = parse_url(url)
    path = parsed_url.path

    return bool(re.search(FILE_REGEX, path))


def clean_url(url, base_url):
    '''
    :param: url - string - URL to clean
    :return: parsed_url - string - Absolute URL without query string
    '''
    if url.startswith("/"):
        url = urljoin(base_url, url)

    parsed_url = parse_url(url)
    scheme = (parsed_url.scheme if parsed_url.scheme else "http") + "://"
    return scheme + parsed_url.netloc + parsed_url.path


def group_urls(response, base_url):
    '''
    :param: response - response - Response object of the request
    :param: base_url - string - base URL to check against
    :return: url_map - dict - A map of the given url with the list of internal, external
    and resource URLs
    '''

    request_url = response.url
    html = document_fromstring(response.text)
    urls = html.iterlinks()
    internal_urls = set()
    external_urls = set()
    resources = set()

    for _, _, url, _ in urls:
        url = clean_url(url, base_url)
        if is_resource(url):
            resources.add(url)
        elif is_same_domain(url, base_url):
            internal_urls.add(url)
        else:
            external_urls.add(url)

    return {"internal_urls": list(internal_urls),
            "external_urls": list(external_urls),
            "resources": list(resources)}

def crawl(url, limit=None):

    sitemap = {}
    base_url = url
    urls_to_crawl = [url]
    crawled_urls = set()
    count = 0

    while urls_to_crawl:
        url = urls_to_crawl.pop(0)
        response = requests.get(url)
        if response.status_code == requests.codes.ok:
            count += 1
            url_map = group_urls(response, base_url)
            sitemap.update({url: url_map})
            crawled_urls.add(url)
            not_crawled_urls = (url for url in url_map["internal_urls"] if url not in crawled_urls)
            urls_to_crawl.extend(not_crawled_urls)

            if limit is not None and count >= limit:
                break

    return sitemap

if __name__ == "__main__":
    pprint.pprint(crawl("http://wiprodigital.com", limit=1))
