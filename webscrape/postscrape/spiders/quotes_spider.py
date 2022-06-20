from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor

class SuperSpider(CrawlSpider):
    name = 'spider'
    allowed_domains = ['quotes.toscrape.com']
    start_urls = ['http://quotes.toscrape.com/']
    base_url = 'http://quotes.toscrape.com'
    rules = [Rule(LinkExtractor(allow = '/'),
                  callback='parse_filter_book', follow=True)]
 
    def parse_filter_book(self, response):
        for quote in response.css('div.quote'):
            yield {
                'Link_without_base_url': quote.xpath('.//span/a/@href').get(),
                'Text': quote.xpath('.//span[@class= "text"]/text()').get(),
                }