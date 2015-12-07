#!/usr/local/bin/python
#-*- encoding:utf-8 -*-
from urllib2 import urlopen,Request
from scrapy import Selector
import requests, json
import random, socket, re

user_agent_list = [\
    'Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.31 (KHTML, like Gecko) Chrome/26.0.1410.43 Safari/537.31',\
    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.17 (KHTML, like Gecko) Chrome/24.0.1312.60 Safari/537.17',\
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_2) AppleWebKit/537.17 (KHTML, like Gecko) Chrome/24.0.1309.0 Safari/537.17',\
    \
    'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.2; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0)',\
    'Mozilla/5.0 (Windows; U; MSIE 7.0; Windows NT 6.0; en-US)',\
    'Mozilla/5.0 (Windows; U; MSIE 6.0; Windows NT 5.1; SV1; .NET CLR 2.0.50727)',\
    \
    'Mozilla/6.0 (Windows NT 6.2; WOW64; rv:16.0.1) Gecko/20121011 Firefox/16.0.1',\
    'Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:15.0) Gecko/20100101 Firefox/15.0.1',\
    'Mozilla/5.0 (Windows NT 6.2; WOW64; rv:15.0) Gecko/20120910144328 Firefox/15.0.2',\
    \
    'Mozilla/5.0 (Windows; U; Windows NT 6.1; rv:2.2) Gecko/20110201',\
    'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9a3pre) Gecko/20070330',\
    'Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10.6; en-US; rv:1.9.2.13; ) Gecko/20101203',\
    \
    'Opera/9.80 (Windows NT 6.0) Presto/2.12.388 Version/12.14',\
    'Opera/9.80 (X11; Linux x86_64; U; fr) Presto/2.9.168 Version/11.50',\
    'Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; de) Presto/2.9.168 Version/11.52',\
    \
    'Mozilla/5.0 (Windows; U; Win 9x 4.90; SG; rv:1.9.2.4) Gecko/20101104 Netscape/9.1.0285',\
    'Mozilla/5.0 (Macintosh; U; PPC Mac OS X Mach-O; en-US; rv:1.8.1.7pre) Gecko/20070815 Firefox/2.0.0.6 Navigator/9.0b3',\
    'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.8.1.12) Gecko/20080219 Firefox/2.0.0.12 Navigator/9.0.0.6',\
    \
    'Mozilla/39.0 (Macintosh; Intel Mac OS X 10_10_4),' \
    'AppleWebKit/536.5 (KHTML, like Gecko)', \
    'Chrome/19.0.1084.54 Safari/536.5'
]

def getSelPage(url):
    """ get selector from url """
    if (url!='') and(url.startswith('http://www.amazon.cn/')):
        try:
            request_headers = { 'User-Agent': random.choice(user_agent_list) }
            request = Request(url, None, request_headers)
            req = urlopen(request, timeout=socket._GLOBAL_DEFAULT_TIMEOUT)
            page = req.read()
            sel = Selector(text=page)
        except:
            req = requests.get(url)
            page = req.text
            sel = Selector(text=page)
    return sel, page


def getASIN(title, author):
    """get asin by book's title and author"""
    index = title + ' ' + author
    url = 'http://www.amazon.cn/s/ref=nb_sb_noss?field-keywords=' + index
    sel, page = getSelPage(url)
    res = sel.xpath('//li[@id="result_0"]/@data-asin').extract()

    if (res != []):
        return res[0]
    else:
        return ''

def getISBN(asin):
    """ get book isbn """
    bookurl = 'http://www.amazon.cn/dp/' + asin
    sel, page = getSelPage(bookurl)
    risbn = re.compile(r'<b>ISBN:</b>[\d, ]*</li>')
    rbarcode = re.compile(r'<b>条形码:</b>[\d ]*</li>')

    barcode = re.findall(rbarcode, page)
    isbnval = re.findall(risbn, page)

    #print barcode
    #print isbnval

    isbn = ''
    if (barcode != []):
        length = len('<b>\xe6\x9d\xa1\xe5\xbd\xa2\xe7\xa0\x81:</b>')
        isbn = barcode[0][length:-5].strip()
        #print '条形码'
    elif (isbnval != []):
        isbn = isbnval[0][13:-5].strip()
    else:
        isbn = ''
    return isbn

def test(title, author):
    if (title!='') and (author!=''):
        asin = getASIN(title, author)
        isbn = getISBN(asin)
        print '%s-->%s' % (asin, isbn)

if (__name__=='__main__'):
    title = '上海私人地圖'
    author = '周佩紅'
    test(title, author)
