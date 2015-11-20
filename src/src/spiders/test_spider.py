# coding=utf-8
import scrapy
from scrapy import signals
from scrapy.xlib.pydispatch import dispatcher

from bs4 import BeautifulSoup
import re
import logging
from urlparse import urlparse
import unirest
import json
from Utility import saveLstToFile

class TestSpider(scrapy.Spider):
    name = "Test"
    allowed_domains = ["shaishufang.com"]
    start_urls = []

    cookie = {
        'shaishufang': 'Mjc5MTYwfGZmY2VmYzIyYmMxZjhlZThjNzgzYjFlOGIxOWUwODg2'
    }

    urlPrefix = 'http://shaishufang.com/index.php/site/main/uid/'
    urlPostfix = '/status//category//friend/false'

    pagePostfix = '/friend/false/category//status//type//page/'
    bookUrlPrefix = 'http://shaishufang.com/index.php/site/detail/uid/'
    bookUrlPostfix = '/status//category/I/friend/false'

    ISBNS = []
    UID = None

    # build start_urls list first
    def __init__(self, uid, *args, **kwargs):
        super(TestSpider, self).__init__(*args, **kwargs)
        dispatcher.connect(self.spider_closed, signals.spider_closed)
        # 'http://shaishufang.com/index.php/site/main/uid/218116/status//category//friend/false'
        url = self.urlPrefix + uid + self.urlPostfix
        self.UID = uid
        self.start_urls.append(url)

    def start_requests(self):
        for i in range(len(self.start_urls)):
            yield scrapy.Request(self.start_urls[i], self.parse, cookies=self.cookie)

    def parse(self, response):
        soup = BeautifulSoup(response.body, "lxml")
        userName = self.getUserName(soup)
        totalPages = self.getTotalPages(soup)
        totalBooks = self.getTotalBooks(soup)

        UID = response.url.replace(self.urlPrefix, '').replace(self.urlPostfix, '')
        for page in range(1, totalPages + 1):
            url = self.urlPrefix + UID + self.pagePostfix + str(page)
            yield scrapy.Request(url, self.parsePage, cookies=self.cookie)

    def parsePage(self, response):
        soup = BeautifulSoup(response.body, "lxml")
        uid = urlparse(response.url).path.split('/')[5]

        bids = self.getUbids(soup)
        for bid in bids:
            url = self.bookUrlPrefix + uid + '/ubid/' + bid + self.bookUrlPostfix
            yield scrapy.Request(url, self.parseBook, cookies=self.cookie)

    def parseBook(self, response):
        soup = BeautifulSoup(response.body, "lxml")
        uid = urlparse(response.url).path.split('/')[5]
        ubid = urlparse(response.url).path.split('/')[7]

        ISBN = self.getISBN(soup)
        # logging.info(uid + ':' + ubid + ':' + ISBN)
        self.ISBNS.append(ISBN)
        # if ISBN:
            # BookItem 包含好多字段，这里只插入ISBN, UID, UBID

    # def __del__(self):
    #     logging.info("spider's destructor")
    #     logging.info(self.ISBNS)
    #     # pass

    def spider_closed(self, spider):
        # logging.info("Spider's destructor")
        logging.info(self.ISBNS)
        saveLstToFile(self.UID + '.csv', self.ISBNS)

    # 从书的详细页面获取ISBN
    def getISBN(self, soup):
        if not soup:
            return False

        if soup.find('div', {'id': 'attr'}):
            if len(soup.find('div', {'id': 'attr'}).find_all('li')) == 0:
                return False
            if "ISBN:" in soup.find('div', {'id': 'attr'}).find_all('li')[-1].text:
                return str(soup.find('div', {'id': 'attr'}).find_all('li')[-1].text.replace('ISBN:', ''))
            else:
                return False

        return False

    # 从书籍列表页面获取UBIDS
    def getUbids(self, soup):
        bids = []
        if not soup:
            return bids

        if soup.find('ul', {'id': 'booksList'}):
            if len(soup.find('ul', {'id': 'booksList'}).find_all('li')) == 0:
                return bids
            for item in soup.find('ul', {'id': 'booksList'}).find_all('li'):
                bids.append(item.attrs['id'])

        return bids

    # 从soup中获取username
    def getUserName(self, soup):
        if not soup:
            return False

        if soup.find('div', {'id': 'username'}):
            return soup.find('div', {'id': 'username'}).find('span').text

        return False

    # 从soup中获取总页数
    def getTotalPages(self, soup):
        if not soup:
            return 1

        if soup.find('ul', {'id': 'booksPage'}):
            if len(soup.find('ul', {'id': 'booksPage'}).find_all('li')) == 0:
                return 1

            return int(soup.find('ul', {'id': 'booksPage'}).find_all('li')[-2].text)

        return 1

    # 从soup中获取总藏书量
    def getTotalBooks(self, soup):
        if not soup:
            return 0

        if soup.find('ul', {'id': 'categoryList'}):
            if soup.find('ul', {'id': 'categoryList'}).find('li'):
                return int(re.sub(r'[^\x00-\x7F]+',' ',soup.find('ul', {'id': 'categoryList'}).find('li').find('a').text).strip())

        return 0
