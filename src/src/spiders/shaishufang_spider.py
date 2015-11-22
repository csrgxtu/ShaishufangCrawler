# coding=utf-8
import scrapy
from bs4 import BeautifulSoup
import re
import logging
from urlparse import urlparse
from ShaishufangHelper import *
from scrapy.conf import settings
from scrapy import signals
from scrapy.xlib.pydispatch import dispatcher

class ShaishufangSpider(scrapy.Spider):
    name = "Shaishufang"
    allowed_domains = ["shaishufang.com"]
    start_urls = []
    handle_httpstatus_list = [404, 403, 407, 502, 503, 505]

    cookie = {
        'shaishufang': settings['COOKIE']
    }

    urlPrefix = 'http://shaishufang.com/index.php/site/main/uid/'
    urlPostfix = '/status//category//friend/false'

    pagePostfix = '/friend/false/category//status//type//page/'
    bookUrlPrefix = 'http://shaishufang.com/index.php/site/detail/uid/'
    bookUrlPostfix = '/status//category/I/friend/false'

    UnvisitedUrls = {'urls': []}
    VisitedUrls = {'urls': []}
    DeadUrls = {'urls': []}
    Datas = {'datas': []}
    Files = {'files': []}

    # build start_urls list first
    def __init__(self, start=0, offset=10, *args, **kwargs):
        super(ShaishufangSpider, self).__init__(*args, **kwargs)
        dispatcher.connect(self.spider_closed, signals.spider_closed)
        self.start_urls = retrieveUnvisitedUrls(start, offset, self.name)

    # when closeing, put all data to master
    def spider_closed(self, spider):
        if len(self.VisitedUrls['urls']) > 0:
            putVisitedUrls(self.VisitedUrls)
        if len(self.Datas['datas']) > 0:
            putDatas(self.Datas)
        if len(self.Files['files']) > 0:
            putFiles(self.Files)
        if len(self.DeadUrls['urls']):
            putDeadUrls(self.DeadUrls)

        logging.info('Inserted VisitedUrls: ' + str(len(self.VisitedUrls)))
        logging.info('Inserted Datas: ' + str(len(self.Datas)))
        logging.info('Inserted Files: ' + str(len(self.Files)))
        logging.info('Inserted DeadUrls: ' + str(len(self.DeadUrls)))

    def start_requests(self):
        for i in range(len(self.start_urls)):
            yield scrapy.Request(self.start_urls[i], self.parse, cookies=self.cookie)

    def parse(self, response):
        if response.status >= 200 and response.status < 400:
            self.VisitedUrls['urls'].append({'url': response.url, 'spider': self.name})

            fileDict = {
                'url': response.url,
                'head': response.headers.to_string(),
                'body': response.body,
                'spider': self.name
            }
            self.Files['files'].append(fileDict)
        else:
            self.DeadUrls['urls'].append({'url': response.url, 'spider': self.name})

        soup = BeautifulSoup(response.body, 'lxml')
        userName = self.getUserName(soup)
        totalPages = self.getTotalPages(soup)
        totalBooks = self.getTotalBooks(soup)

        userDict = {
            'UID': response.url.replace(self.urlPrefix, '').replace(self.urlPostfix, ''),
            'UserName': userName,
            'TotalBooks': totalBooks,
            'TotalPages': totalPages
        }
        dataDict = {
            'url': response.url,
            'spider': self.name,
            'data': userDict
        }
        self.Datas['datas'].append(dataDict)

        UID = response.url.replace(self.urlPrefix, '').replace(self.urlPostfix, '')
        for page in range(1, totalPages + 1):
            url = self.urlPrefix + UID + self.pagePostfix + str(page)
            yield scrapy.Request(url, self.parsePage, cookies=self.cookie)

    def parsePage(self, response):
        soup = BeautifulSoup(response.body, 'lxml')
        uid = urlparse(response.url).path.split('/')[5]

        bids = self.getUbids(soup)
        for bid in bids:
            url = self.bookUrlPrefix + uid + '/ubid/' + bid + self.bookUrlPostfix
            yield scrapy.Request(url, self.parseBook, cookies=self.cookie)

    def parseBook(self, response):
        soup = BeautifulSoup(response.body, 'lxml')
        uid = urlparse(response.url).path.split('/')[5]
        ubid = urlparse(response.url).path.split('/')[7]

        ISBN = self.getISBN(soup)
        if ISBN:
            bookDict = {
                'ISBN': ISBN,
                'UID': uid,
                'UBID': ubid
            }
            dataDict = {
                'url': response.url,
                'spider': self.name,
                'data': bookDict
            }
            self.Datas['datas'].append(dataDict)

            fileDict = {
                'url': response.url,
                'head': response.headers.to_string(),
                'body': response.body,
                'spider': self.name
            }
            self.Files['files'].append(fileDict)


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
