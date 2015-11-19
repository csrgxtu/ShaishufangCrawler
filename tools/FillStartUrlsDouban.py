#!/usr/bin/env python
# coding=utf-8
# Author: Archer Reilly
# File: FillStartUrls.py
# Date: 18/Nov/2015
# Desc: fill the master unvisitedurls
#
# Produced By BR
import pymongo
from pymongo import MongoClient

client = MongoClient('192.168.100.3', 27019)
db = client['master']

db['unvisited'].create_index([('url', pymongo.DESCENDING), ('spider', pymongo.DESCENDING)])
db['visited'].create_index([('url', pymongo.DESCENDING), ('spider', pymongo.DESCENDING)])
db['dead'].create_index([('url', pymongo.DESCENDING), ('spider', pymongo.DESCENDING)])
db['data'].create_index([('url', pymongo.DESCENDING), ('spider', pymongo.DESCENDING)])
db['file'].create_index([('url', pymongo.DESCENDING), ('spider', pymongo.DESCENDING)])

with open('./isbns.data', 'r') as MH:
    for line in MH:
        isbn = line.replace("\n", "")
        print 'Insrted: ', isbn
        url = 'http://book.dobuan.com/isbn/' + isbn
        db.['unvisited'].insert({'url': url, 'spider': 'douban'})
