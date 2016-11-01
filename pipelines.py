# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from __future__ import unicode_literals
import json
import codecs
import os
import time


class CommonCrawlerPipeline(object):
    # def process_item(self, item, spider):
    #     return item

    def __init__(self):

        # if not os.path.isfile(os.getcwd() + '/finance_crawler/naver.json'):
        #     with open(os.getcwd() + '/finance_crawler/naver.json', 'w') as f:
        #         pass

        # 크롤링 데이터를 저장할 파일 OPEN
        # if os.path.isdir(os.path.join(os.path.abspath('.'), 'vjvj_crawler')):
        #     path_store = os.path.join(os.path.abspath("."), 'vjvj_crawler', 'result.json')
        # else:
        path_store = os.path.join(os.path.abspath("."), 'result.json')

        self.file = codecs.open(path_store, 'a', encoding='utf-8')

    def process_item(self, item, spider):
        # Item 을 한줄씩 구성
        line = json.dumps(dict(item), ensure_ascii=False) + "\n"
        # 파일에 기록
        self.file.write(line)
        return item

    def spider_closed(self, spider):
        # 파일 CLOSE
        self.file.close()

