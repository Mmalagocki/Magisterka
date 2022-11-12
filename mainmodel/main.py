import sys
import json
import pandas as pd
from scrapy.crawler import CrawlerProcess

sys.path.append("../urlmodel/")
sys.path.append("../webscrape/postscrape/spiders")

from urlmodel import UrlModel
from spider import SuperSpider


def main():

    # process = CrawlerProcess()
    # process.crawl(SuperSpider)
    # process.start()
    df = pd.read_json (r'C:\Users\BeLia\OneDrive\Dokumenty\Studia\Magisterka\webscrape\postscrape\spiders\results.json')
    x = UrlModel()
    x.train()

if __name__ == '__main__':
    main()