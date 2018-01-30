# -*- coding: utf-8 -*-
import scrapy

from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

'''
Crawl quotes data
@example
    scrapy crawl quotes
    scrapy crawl quotes -a debug=1
    scrapy crawl quotes -L DEBUG
'''
class QuotesSpider(scrapy.Spider):
    name = 'quotes'

    '''
    Custome pipelines for this pipeline
    '''
    custom_settings = {
        'ITEM_PIPELINES': {
            'crawler.pipelines.FilePipeline': 1,
        }
    }

    def __init__(self, debug=None, *args, **kwargs):
        '''
        Initialize parent spider here for init @tracer.log
        '''
        super(QuotesSpider, self).__init__(*args, **kwargs)

        '''
        Get input args 
        '''
        self.debug = debug

    '''
    Another way to add urls to the crawl queue
    You can query urls from database and add to queue here
    '''
    def start_requests(self):
        urls = [
            'http://quotes.toscrape.com/page/1/',
            'http://quotes.toscrape.com/page/2/',
        ]

        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):

        if self.debug:
            self.logger.info('Crawl success: %s', response.url)

        for quote in response.css('div.quote'):
            yield {
                '_file': 'storage/quotes.json',
                '_mode': 'w',
                'text': quote.css('span.text::text').extract_first(),
                'author': quote.css('span small::text').extract_first(),
                'tags': quote.css('div.tags a.tag::text').extract(),
            }
