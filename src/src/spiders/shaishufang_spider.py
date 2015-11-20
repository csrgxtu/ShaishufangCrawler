# coding=utf-8
import scrapy
from bs4 import BeautifulSoup
import re
import logging
from urlparse import urlparse
import unirest
import json

class ShaishufangSpider(scrapy.Spider):
    name = "Shaishufang"
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

    # build start_urls list first
    def __init__(self, start=0, offset=10, *args, **kwargs):
        super(ShaishufangSpider, self).__init__(*args, **kwargs)
        url = 'http://192.168.100.3:5000/unvisitedurls?start=' + str(start) + '&offset=' + str(offset) + '&spider=' + self.name
        headers = {
            "Accept": "application/json",
        }
        res = unirest.post(url, headres=headers)
        for url in res.body['data']:
            self.start_urls.append(url['url'])

    def start_requests(self):
        for i in range(len(self.start_urls)):
            yield scrapy.Request(self.start_urls[i], self.parse, cookies=self.cookie)

    def parse(self, response):
        if response.status >= 200 and response.status < 400:
            url = 'http://192.168.100.3:5000/visitedurls'
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
                logging.info("Visisted Inserted: " + json.dumps(params))

            fileUrl = 'http://192.168.100.3:5000/file'
            fileDict = {
                'url': response.url,
                'head': response.headers.to_string(),
                'body': response.body,
                'spider': self.name
            }
            params = {
                'files': [
                    fileDict
                ]
            }
            res = unirest.put(fileUrl, headers=headers, params=json.dumps(params))
            if res.body['code'] == 200:
                logging.info('File Inserted: ' + res.body['data'][0])
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

        soup = BeautifulSoup(response.body, "lxml")
        userName = self.getUserName(soup)
        totalPages = self.getTotalPages(soup)
        totalBooks = self.getTotalBooks(soup)

        self.userOrBook = 'User'
        userDict = {
            'UID': response.url.replace(self.urlPrefix, '').replace(self.urlPostfix, ''),
            'UserName': userName,
            'TotalBooks': totalBooks,
            'TotalPages': totalPages
        }
        url = 'http://192.168.100.3:5000/data'
        headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        }
        params = {
            'datas': [
                {
                    'url': response.url,
                    'spider': self.name,
                    'data': userDict
                }
            ]
        }
        res = unirest.put(url, headers=headers, params=json.dumps(params))
        if res.body['code'] == 200:
            logging.info("Data Inserted: " + json.dumps(params))

        # logging.info(userItem)

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
        if ISBN:
            # BookItem 包含好多字段，这里只插入ISBN, UID, UBID
            # bookItem = BookItem()
            # bookItem['ISBN'] = ISBN
            # bookItem['UID'] = uid
            # bookItem['UBID'] = ubid
            self.userOrBook = 'Book'
            # yield bookItem
            bookDict = {
                'ISBN': ISBN,
                'UID': uid,
                'UBID': ubid
            }
            url = 'http://192.168.100.3:5000/data'
            headers = {
                'Content-Type': 'application/json',
                'Accept': 'application/json'
            }
            params = {
                'datas': [
                    {
                        'url': response.url,
                        'spider': self.name,
                        'data': bookDict
                    }
                ]
            }
            res = unirest.put(url, headers=headers, params=json.dumps(params))
            if res.body['code'] == 200:
                logging.info('Data Inserted: ' + json.dumps(params))

            fileDict = {
                'url': response.url,
                'head': response.headers.to_string(),
                'body': response.body,
                'spider': self.name
            }

            fileUrl = 'http://192.168.100.3:5000/file'
            params = {
                'files': [
                    fileDict
                ]
            }
            res = unirest.put(fileUrl, headers=headers, params=json.dumps(params))
            if res.body['code'] == 200:
                logging.info('File Inserted: ' + res.body['data'][0])

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
