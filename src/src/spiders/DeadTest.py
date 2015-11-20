# coding=utf-8
import scrapy
from bs4 import BeautifulSoup
import re
import logging
from urlparse import urlparse
import unirest
import json
# from src.items import UserItem, BookItem

class DeadtestSpider(scrapy.Spider):
    name = "Deadtest"
    allowed_domains = ["shaishufang.com"]
    start_urls = []
    handle_httpstatus_list = [404, 403]

    # build start_urls list first
    def __init__(self, url, *args, **kwargs):
        super(DeadtestSpider, self).__init__(*args, **kwargs)
        self.start_urls.append(url)
        logging.info(self.start_urls[0])

    def start_requests(self):
        # for i in range(len(self.start_urls)):
        yield scrapy.Request(self.start_urls[0], self.parse)

    def parse(self, response):
        logging.info(response.status)
        if response.status == 200:
            logging.info('Status code: ' + str(response.status))
        else:
            url = 'http://192.168.100.3:5000/deadurls'
            headers = {
                'Accept': 'application/json',
                "Content-Type": "application/json"
            }
            params = {
                "urls": [
                    {"url": response.url, "spider": self.name}
                ]
            }
            res = unirest.put(url, headers=headers, params=json.dumps(params))
            if res.body['code'] == 200:
                logging.info("Dead Inserted: " + json.dumps(params))
