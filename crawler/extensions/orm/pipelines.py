# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import time
import json
import scrapy
import logging

from .connection import from_settings
from scrapy.exceptions import DropItem
from sqlalchemy import text
from sqlalchemy.orm import sessionmaker, load_only

logger = logging.getLogger(__name__)

class DatabasePipeline(object):

    model = None

    def __init__(self, crawler):
        '''
        Access the crawler instance
        '''
        self.crawler  = crawler
        self.stats    = crawler.stats
        self.settings = crawler.settings

        '''
        Initialize database connection
        '''
        self.session = sessionmaker(bind=from_settings(self.settings))

    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler)

    def process_item(self, item, spider):
        ''' Create new session connect to database '''
        session = self.session()

        data  = item.copy()
        key   = data.pop('_id', None)
        table = data.pop('_table', None)
        
        '''
        Remove all helper keys
        '''
        for k in data.keys():
            if '_' in k:
                data.pop(k)

        '''
        Check for valid pipeline item
        '''
        if not key or not table:
            return item

        '''
        Check and write data to table
        query = text("SELECT id FROM %s WHERE id=:id LIMIT 1" % table);
        found = session.execute(query, {'id': key})
        '''
        data  = json.dumps(dict(data))
        query = text("UPDATE %s SET data=:data, updated=:updated WHERE id=:id" % table);
        result = session.execute(query, {'id': key, 'data': data, 'updated': time.time()})
        
        session.commit()

        if int(result.rowcount) == 0:
            query = text("INSERT INTO %s(id, data, created, updated) VALUES(:id, :data, :created, :updated)" % table);
            session.execute(query, {'id': key, 'data': data, 'created': time.time(), 'updated': time.time()})
            session.commit()

        ''' Close session connect to database '''
        session.close()

        return item
