import sys
import json
import pandas as pd
import tensorflow as tf 

from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings



sys.path.append("../urlmodel/")
sys.path.append("../webscrape/postscrape/spiders")

from urlmodel import UrlModel
from spider import SuperSpider

def main():
    # process = CrawlerProcess()
    # process = CrawlerProcess(get_project_settings())
    # process.crawl('spider', domain='scrapy.org')
    # process.start()

    df = pd.read_json (r'C:\Users\BeLia\Documents\Magisterka\webscrape\postscrape\spiders\results.json')
    urlmodel = UrlModel()
    urlmodel.verify()
    

if __name__ == '__main__':
    main()