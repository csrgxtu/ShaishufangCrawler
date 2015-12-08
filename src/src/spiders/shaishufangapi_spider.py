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
    TotalBooks = 0

    #Headers = {'Authorization': 'Basic Mjc5MTYwOjAxNjIxYjE5NjE0YTdjZTM0YTJkODIxNzdiMGYzNDY5'}
    Headers = {}

    # APILogin = 'http://121.41.60.81/index.php/api2/account/verify_credentials/'
    APIPrefix = 'http://121.41.60.81/index.php/api2/bookroom/books/list?uid='
    APIPostfix = '&shortCategory=all&page_index=0&page_size=0&fmt=xml'

    # build start_urls list first
    def __init__(self, uid, *args, **kwargs):
        super(ShaishufangAPISpider, self).__init__(*args, **kwargs)
        dispatcher.connect(self.spider_closed, signals.spider_closed)
        self.UID = uid
        url = self.APIPrefix + str(uid) + self.APIPostfix
        self.start_urls.append(url)

    def start_requests(self):
        for i in range(len(self.start_urls)):
            yield scrapy.Request(self.start_urls[i], self.parse, headers=self.Headers)

    def parse(self, response):
        obj = xmltodict.parse(response.body)
        logging.info('Declared Total Books: ' + str(int(obj['response']['result']['total'])))
        # everytime, request 500 books from the api
        pageNum = 0
        if (int(obj['response']['result']['total']) % 500) > 0:
            pageNum = int(obj['response']['result']['total'])/500 + 1

        logging.info('TotalPageNum: ' + str(pageNum))
        for page in range(1, pageNum + 1):
            url = self.APIPrefix + str(self.UID) + '&shortCategory=all&fmt=xml&page_size=500&page_index=' + str(page)
            # logging.info(url)
            yield scrapy.Request(url, self.parsePage, headers=self.Headers)

        # soup = BeautifulSoup(response.body, "lxml")
        # userName = self.getUserName(soup)
        # totalPages = self.getTotalPages(soup)
        # totalBooks = self.getTotalBooks(soup)
        #
        # UID = response.url.replace(self.urlPrefix, '').replace(self.urlPostfix, '')
        # for page in range(1, totalPages + 1):
        #     url = self.urlPrefix + UID + self.pagePostfix + str(page)
        #     yield scrapy.Request(url, self.parsePage, cookies=self.cookie)

    def parsePage(self, response):
        obj = xmltodict.parse(response.body)
        logging.info('Books: ' + str(len(obj['response']['result']['books']['item'])))
        self.TotalBooks = self.TotalBooks + len(obj['response']['result']['books']['item'])

        for book in obj['response']['result']['books']['item']:
            # self.ISBNS.append(str(book['isbn']))
            # logging.info(book['isbn'])
            if book['isbn'] != None:
                self.ISBNS.append(book['isbn'])
        # pass

    def spider_closed(self, spider):
        # logging.info("Spider's destructor")
        # logging.info(self.ISBNS)
        # saveMatrixToFile(self.UID + '.csv', self.Books)
        # pass
        logging.info('Actual Total Books: ' + str(self.TotalBooks))
        logging.info('Isbns in ISBNS: ' + str(len(self.ISBNS)))
        saveLstToFile(self.UID + '.csv', self.ISBNS)
