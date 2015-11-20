# coding=utf-8
# Author: Archer Reilly
# Date: 20/Nov/2015
# File: Shaishufang.py
# Desc: help class for Shaishufang Spider
#
# Produced By BR
import unirest
import json
from scrapy.conf import settings
import logging

BaseUrl = settings['API_HOST']
Headers = {
    'Content-Type': 'application/json',
    'Accept': 'application/json'
}

# getUrls will get urls from master
def getUnvisitedUrls(start, offset, spider):
    url = BaseUrl + 'unvisitedurls?start=' + str(start) + '&offset=' + str(offset) + '&spider=' + spider
    res = unirest.get(url, headers=Headers)
    if res.body['code'] != 200:
        return []

    if len(res.body['data']) == 0:
        return []

    urls = []
    for item in res.body['data']:
        urls.append(str(item['url']))

    return urls

# retrieveUrls will retrieve urls from master
def retrieveUnvisitedUrls(start, offset, spider):
    url = BaseUrl + 'unvisitedurls?start=' + str(start) + '&offset=' + str(offset) + '&spider=' + spider
    res = unirest.post(url, headers=Headers)
    if res.body['code'] != 200:
        return []

    if len(res.body['data']) == 0:
        return []

    urls = []
    for item in res.body['data']:
        urls.append(str(item['url']))

    return urls

# putUnvisitedUrls will put data dict to master
# data: {'urls': [{'url': 'http://w.g.com', 'spider': 'Shaishufan'}]}
def putUnvisitedUrls(data):
    url = BaseUrl + 'unvisitedurls'
    res = unirest.put(url, headers=Headers, params=json.dumps(data))

    if res.body['code'] != 200:
        return False

    return True

# # getVisitedUrls will get url list from master
# def getVisitedUrls(start, offset, spider):
#     pass
#
# # retrieveVisitedUrls will retrieve url list from master
# def retrieveVisitedUrls(start, offset, spider):
#     pass

# putVisitedUrls will put a list visited urls to master
# data: {'urls': [{'url': 'http://w.g.com', 'spider': 'Shaishufan'}]}
def putVisitedUrls(data):
    url = BaseUrl + 'visitedurls'
    res = unirest.put(url, headers=Headers, params=json.dumps(data))

    if res.body['code'] != 200:
        return False

    return True

# putDeadUrls will put a list dead urls to master
# data: {'urls': [{'url': 'http://w.g.com', 'spider': 'Shaishufang'}]}
def putDeadUrls(data):
    url = BaseUrl + 'deadurls'
    res = unirest.put(url, headers=Headers, params=json.dumps(data))

    if res.body['code'] != 200:
        return False

    return True

# putDatas will put a list datas to master
# data: {
#   'datas': [
#      {'url': 'http://w.g.com', 'spider': 'Shaishufang', 'data': dataItem}
#   ]
# }
# dataItem: your own dict
def putDatas(data):
    url = BaseUrl + 'data'
    res = unirest.put(url, headers=Headers, params=json.dumps(data))

    if res.body['code'] != 200:
        return False

    return True

# putFiles will put a list files to master
# data: {
#   'files': [
#       {'url': 'http://w.g.com', 'spider': 'Shaishufang', 'head': 'my head', 'body': 'my body'}
#   ]
# }
def putFiles(data):
    url = BaseUrl + 'file'
    res = unirest.put(url, headers=Headers, params=json.dumps(data))

    if res.body['code'] != 200:
        return False

    return True
