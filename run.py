from pprint import pprint
import argparse

from crawler.crawler import crawl


if __name__ == "__main__":
    parser=argparse.ArgumentParser(description='''A simple web cralwer''')
    parser.add_argument('--url', help='URL to crawl', required=True)
    parser.add_argument('--limit', type=int, default=1, help='Number of internal URLs to crawl')
    args=parser.parse_args()
    pprint(crawl(args.url, args.limit))
