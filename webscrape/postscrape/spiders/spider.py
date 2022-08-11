from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.shell import inspect_response


class SuperSpider(CrawlSpider):
    name = 'spider'
    allowed_domains = ['zthplanet.com']
    start_urls = ['http://zthplanet.com/']
    base_url = 'http://zthplanet.com'

    # allowed_domains = ['https://webscraper.io/test-sites/e-commerce/allinone']
    # start_urls = ['https://webscraper.io/test-sites/e-commerce/allinone']
    # base_url = 'https://webscraper.io/test-sites/e-commerce/allinone'

    rules = [Rule(LinkExtractor(allow='/'),
                  callback='parse', follow=True)]

    def parse(self, response):
        url_list = []
        for quote in response.css('div'):
            names =  quote.xpath('.//a/@href').getall()
            for name in names:
                if name in url_list:
                    continue
                url_list.append(name)
                yield {
                    'examined page': name,
                }