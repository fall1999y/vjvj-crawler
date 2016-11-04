# coding=utf-8
import scrapy
import os
import re
from configparser import ConfigParser

from vjvj_crawler.items import CommonCrawlerItem
from datetime import datetime

__author__ = 'fall1999y'


class CommonSpider(scrapy.Spider):
    def parse(self, response):
        pass

    name = "common_spider"

    # allowed_domains = ["naver.com"]
    # start_urls = []

    def __init__(self, section, *args, **kwargs):

        super(CommonSpider, self).__init__(*args, **kwargs)

        # self.base_source_path = os.path.abspath('vjvj_crawler')
        # if not os.path.exists(self.base_source_path):
        self.base_source_path = os.path.abspath('.')

        self.config = ConfigParser()
        # self.config = configparser.RawConfigParser()
        path_config = os.path.join(self.base_source_path, 'config', 'config.properties')
        self.config.read(path_config)

        # 'TARGET_INFO'
        # section = section and 'TARGET_INFO' or section
        self.section = section
        self.parsing_url = str(self.config.get(section, 'parsing_url')).replace('__page__', '%d')
        limit_page = int(self.config.get(section, 'limit_page'))

        '''limit_page 미만 (포함 안됨)'''
        # self.crawling_range = range(1, limit_page, 1)
        '''limit_page 이하 (포함)'''
        self.crawling_range = range(limit_page)
        self.regex_article = str(self.config.get(section, 'regex_article'))
        self.regex_title = str(self.config.get(section, 'regex_title'))
        self.regex_seq = str(self.config.get(section, 'regex_seq'))
        self.acc = 0
        self.items = []

    def start_requests(self):
        # yield scrapy.Request(url, self.parse_client, method="POST", body=payload)
        for i in self.crawling_range:
            # % i 공백 주의
            yield scrapy.Request(self.parsing_url % i, self.parse_client)

    def parse_client(self, response):
        # filename = os.getcwd() + '/vjvj_crawler/page.txt'
        # path_max_seq_store = os.path.join(self.base_source_path, 'max_article.txt')

        compare_date = self.config.has_option(self.section, 'read_date') and str(self.config.get(self.section,
                                                                                                 "read_date")) or None

        #
        # if os.path.isfile(path_max_seq_store):
        #     with open(path_max_seq_store, 'r') as f:
        #         compare_date = f.readline()
        #
        p = re.compile(r'\t|\n')
        for sel in response.xpath(self.regex_article):
            item = CommonCrawlerItem()
            # item['title'] = sel.xpath('a/div/text()').extract()[0]
            item['title'] = p.sub("", sel.xpath(self.regex_title).extract()[0])

            # datetime.strptime string 을 date 형으로 형변환
            # date = datetime.strptime(sel.xpath('td[1]/span/text()').extract(), "%Y.%m.%d %H:%M")
            # item['date'] = date.strftime('%Y-%m-%d %H:%M')
            item['date'] = sel.xpath(self.regex_seq).extract()[0]

            if not compare_date or item['date'] > compare_date:
                self.items.append(item)

        self.acc += 1

        if self.acc >= self.crawling_range.stop - 1:
            sorted_items = sorted(self.items, key=lambda i: i['date'])

            if len(sorted_items) > 0:
                for item in sorted_items:
                    yield item

                max_date = sorted_items[len(sorted_items) - 1]['date']

                print(os.path.join(self.base_source_path, 'config', 'config.properties'))
                with open(os.path.join(self.base_source_path, 'config', 'config.properties'), 'w+') as configfile:
                    configfile.write("# __page__ 는 range(limit_page) 에 의해 치환됨\n")
                    self.config.set(self.section, 'read_date', max_date)
                    self.config.write(configfile)

                    #
                    # with open(path_max_seq_store, 'w') as f:
                    #     f.write(max_date)
                    #     # items = sorted(items, key=lambda item : item['date'])
                    #     # print(items)

                # 원본저장 (url의 내용 통째로 저장)
                with open(os.path.join(self.base_source_path, 'result', 'temp',
                                       self.section + '_' + re.sub(r'\W', '', str(max_date)) + '.txt'), 'wb') as f:
                    f.write(response.body)
