# coding=utf-8
import scrapy
from bs4 import BeautifulSoup
import logging
import re

class ShaishufangSpider(scrapy.Spider):
    name = "Shaishufang"
    allowed_domains = ["shaishufang.com"]
    start_urls = []

    # build start_urls list first
    def __init__(self):
        urlPrefix = 'http://shaishufang.com/index.php/site/main/uid/'
        urlPostfix = '/status//category//friend/false'
        for i in range(1, 3):
            self.start_urls.append(urlPrefix + str(i) + urlPostfix)

    def start_requests(self):
        for i in range(len(self.start_urls)):
            yield scrapy.Request(self.start_urls[i], cookies={'shaishufang': 'Mjc5MTYwfGZmY2VmYzIyYmMxZjhlZThjNzgzYjFlOGIxOWUwODg2'})

    def parse(self, response):
        soup = BeautifulSoup(response.body)
        userName = self.getUserName(soup)
        totalPages = self.getTotalPages(soup)
        totalBooks = self.getTotalBooks(soup)
        logging.info(userName)
        logging.info(totalBooks)
        logging.info(totalPages)

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
            return 0

        if soup.find('ul', {'id': 'booksPage'}):
            if len(soup.find('ul', {'id': 'booksPage'}).find_all('li')) == 0:
                return 0

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
