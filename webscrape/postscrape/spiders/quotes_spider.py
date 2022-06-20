from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.shell import inspect_response


class SuperSpider(CrawlSpider):
    name = 'spider'
    allowed_domains = ['quotes.toscrape.com']
    start_urls = ['http://quotes.toscrape.com/']
    base_url = 'http://quotes.toscrape.com'

    # allowed_domains = ['https://webscraper.io/test-sites/e-commerce/allinone']
    # start_urls = ['https://webscraper.io/test-sites/e-commerce/allinone']
    # base_url = 'https://webscraper.io/test-sites/e-commerce/allinone'

    rules = [Rule(LinkExtractor(allow='/'),
                  callback='parse', follow=True)]

    def parse(self, response):
        url_list = []
        for quote in response.css('div'):
            name =  quote.xpath('.//a/@href').get()
            if name in url_list:
                continue
            url_list.append(name)
            yield {
                'Link_without_base_url': quote.xpath('.//a/@href').get(),
                'Text':  response.css("::text").extract(),
            }