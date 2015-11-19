#!/usr/bin/env python
# coding=utf-8
# Author: Archer Reilly
# File: FillStartUrls.py
# Date: 18/Nov/2015
# Desc: fill the master unvisitedurls
#
# Produced By BR
import unirest
import json

headers = {
    'Accept': 'application/json',
    "Content-Type": "application/json"
}

# first, shaishufang
# http://shaishufang.com/index.php/site/main/uid/2/status//category//friend/false
API = 'http://192.168.100.3:5000/unvisitedurls'
# API = 'http://127.0.0.1:5000/unvisitedurls'
urlPrefix = 'http://shaishufang.com/index.php/site/main/uid/'
urlPostfix = '/status//category//friend/false'
for uid in range(1, 279653):
    url = urlPrefix + str(uid) + urlPostfix
    params = {
        "urls": [
            {
                "url": url,
                "spider": 'Shaishufang'
            }
        ]
    }
    response = unirest.put(API, headers=headers, params=json.dumps(params))
    print response.body
