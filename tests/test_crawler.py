import json
import responses
import requests

from crawler.crawler import *

def test_form_url():
    assert form_url("http://google.com") == "http://google.com"
    assert form_url("www.google.com") == "http://www.google.com"

def test_clean_url():
    base_url = "www.google.com"
    assert clean_url("http://google.com?q=1", base_url) == "http://google.com"
    assert clean_url("www.google.com", base_url) == "http://www.google.com"

def test_is_same_domain():
    base_url = "google.com"
    assert is_same_domain("http://google.com?q=1", base_url)
    assert not is_same_domain("www.google.com", "example.com")

def test_is_resource():
    base_url = "google.com"
    assert is_resource("http://google.com/test.img")
    assert not is_resource("www.google.com/test/")

@responses.activate
def test_crawl():
    with open('tests/httpbin.html') as f:
        responses.add(responses.GET, 'http://httpbin.org', body=f.read(), status=200)

    with open('tests/httpbin.json') as f:
        return_dict = json.loads(f.read())

    url = 'http://httpbin.org'
    grouped_urls = crawl(url, limit=1)
    assert sorted(grouped_urls[url]["internal_urls"]) == sorted(return_dict[url]["internal_urls"])
    assert sorted(grouped_urls[url]["external_urls"]) == sorted(return_dict[url]["external_urls"])
    assert sorted(grouped_urls[url]["resources"]) == sorted(return_dict[url]["resources"])
