# -*- coding: utf-8 -*-
import re
import scrapy

from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

'''
Crawl stackoverflow list questions
@example
    scrapy crawl stack
    scrapy crawl stack -a debug=1
    scrapy crawl stack -L DEBUG
'''
class StackSpider(scrapy.Spider):

    name = 'stack'

    '''
    Define allowed domains here
    '''
    allowed_domains = [
        'stackoverflow.com'
    ]

    '''
    Define start urls here
    '''
    start_urls = [
        'https://stackoverflow.com/questions?pagesize=50&sort=newest'
    ]

    rules = (
        Rule(LinkExtractor(allow=r'questions\?page=[0-2]&sort=newest'),
             callback='parse', follow=True),
    )

    custom_settings = {
        'ITEM_PIPELINES': {
            'crawler.pipelines.FilePipeline': 1,
            'crawler.extensions.orm.DatabasePipeline': 2,
        }
    }

    def __init__(self, debug=None, *args, **kwargs):
        '''
        Initialize parent spider here for init @tracer.log
        '''
        super(StackSpider, self).__init__(*args, **kwargs)

        '''
        Get input args 
        '''
        self.debug = debug

    '''
    Parse list questions to get question detail data
    '''
    def parse(self, response):
        questions = response.xpath('//div[@class="summary"]')

        for question in questions:
            '''
            Parse question item link
            '''
            url = question.xpath('h3/a[@class="question-hyperlink"]/@href').extract_first()
            link = response.urljoin(url)

            '''
            Push qestion data to pipelines
            '''
            item = {}

            '''
            Save to json file
            '''
            item['_file'] = 'storage/newest.json'
            item['_mode'] = 'w'

            '''
            Save data section
            '''
            item['id'] = self.qid(url)
            item['title'] = question.xpath('h3/a[@class="question-hyperlink"]/text()').extract_first()
            item['link'] = link
            item['excerpt'] = question.xpath('div[@class="excerpt"]/text()').extract_first()

            yield item

            '''
            Add qestion detail to queue to crawl
            '''
            yield scrapy.Request(url=link, meta={'qid': item['id']}, callback=self.parse_question)

        if self.debug:
            self.logger.info('Crawl question list: %s', response.url)

    def parse_question(self, response):
        '''
        Get question id from meta
        '''
        qid = response.meta.get('qid') or 0

        '''
        Parse question detail data
        '''
        item = {}

        '''
        Save to table:questions
        '''
        item['_id'] = qid
        item['_table'] = 'questions'

        '''
        Save to json file
        '''
        item['_file'] = 'storage/questions.json'
        item['_mode'] = 'w'

        '''
        Question data save
        '''
        item['id'] = qid
        item['title'] = response.css('#question-header h1 a::text').extract_first()
        item['link'] = response.url
        item['question'] = response.css('.question .post-text').extract_first()

        yield item

        '''
        Parse answers data
        '''
        answers = response.xpath('//div[@id="answers"]/div[contains(@class, "answer")]')

        for answer in answers:
            aid = answer.xpath('//@data-answerid').extract_first()

            if not aid:
                continue

            aid = int(aid)
            
            item = {}
        
            '''
            Save to table:answers
            '''
            item['_id'] = aid
            item['_table'] = 'answers'

            '''
            Save to json file
            '''
            item['_file'] = 'storage/answers.json'
            item['_mode'] = 'w'

            '''
            Answer data save
            '''
            item['id'] = aid
            item['qid'] = qid
            item['link'] = response.urljoin(answer.xpath('..//a[@class="short-link"]/@href').extract_first())
            item['answer'] = answer.css('.answercell .post-text').extract_first()

            yield item

        if self.debug:
            self.logger.info('Crawl answers list: %s', response.url)

    '''
    Get question id from url
    @example
        /questions/48512763/how-to-insert-different-information-without-deleting-the-previous-one-in-firebas
    '''
    def qid(self, link):
        m = re.search(u'/([\d]+)/', link)
        if m:
            return int(m.group(1).strip())

