#!/usr/local/bin/python
#-*- encoding:utf-8 -*-
import sys, os
import pymongo
from pymongo import MongoClient

import csv, json

def getISBN(title, author, spider='douban'):
    """ get isbn by search douban data collection """
    # client
    client = MongoClient(host='192.168.100.3', port=27019)

    # database
    master = client.master

    # collection
    data = master.data

    cur = data.find({
                        "$and":
                        [
                            {"spider":spider},
                            {"data.书名":title},
                            {"data.作者":author}
                        ]
                    })

    # isbn
    isbn = ''
    curcnt = cur.count()
    if (curcnt==1):
        try:
            isbn = cur[0]["data"]["ISBN"]
        except:
            isbn = ''
        #print 'oh yeah!'
    else:
        for c in cur:
            try:
                isbn = c["data"]["ISBN"]
            except:
                isbn = ''
        #print "oops, my god!"

    return isbn

def test(title, author):
    if (title !='') and (author != ''):
        isbn = getISBN(title, author, spider='douban')
        print title, author, isbn

if (__name__=='__main__'):
    title = '汉书集释（全十二册）'
    author = '施之勉'
    test(title, author)
