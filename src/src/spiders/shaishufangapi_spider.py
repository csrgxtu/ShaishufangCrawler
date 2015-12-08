# coding=utf-8
import scrapy
from scrapy import signals
from scrapy.xlib.pydispatch import dispatcher

import logging
from Utility import saveLstToFile
import xmltodict

class ShaishufangAPISpider(scrapy.Spider):
    name = "ShaishufangAPI"
    start_urls = []

    http_user = '279160'
    http_pass = '01621b19614a7ce34a2d82177b0f3469'

    ISBNS = []
    UID = None

    APILogin = 'http://121.41.60.81/index.php/api2/account/verify_credentials/'
    APIPrefix = 'http://121.41.60.81/index.php/api2/bookroom/books/list?uid='
    APIPostfix = '&shortCategory=all&page_index=0&page_size=1&fmt=xml'

    # build start_urls list first
    def __init__(self, uid, *args, **kwargs):
        super(ShaishufangAPISpider, self).__init__(*args, **kwargs)
        dispatcher.connect(self.spider_closed, signals.spider_closed)
        self.UID = uid
        url = self.APIPrefix + str(uid) + self.APIPostfix
        self.start_urls.append(url)

    def start_requests(self):
        for i in range(len(self.start_urls)):
            yield scrapy.Request(self.start_urls[i], self.parse)

    def parse(self, response):
        obj = xmltodict.parse(response.body)
        logging.info(int(obj['response']['result']['total']))


        # soup = BeautifulSoup(response.body, "lxml")
        # userName = self.getUserName(soup)
        # totalPages = self.getTotalPages(soup)
        # totalBooks = self.getTotalBooks(soup)
        #
        # UID = response.url.replace(self.urlPrefix, '').replace(self.urlPostfix, '')
        # for page in range(1, totalPages + 1):
        #     url = self.urlPrefix + UID + self.pagePostfix + str(page)
        #     yield scrapy.Request(url, self.parsePage, cookies=self.cookie)


    def spider_closed(self, spider):
        # logging.info("Spider's destructor")
        # logging.info(self.ISBNS)
        # saveLstToFile(self.UID + '.csv', self.ISBNS)
        # saveMatrixToFile(self.UID + '.csv', self.Books)
        pass
