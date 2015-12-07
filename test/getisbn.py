#!/usr/bin/env python
#-*- encoding:utf-8 -*-
import getisbnBydouban
import getisbnByamazon
from pymongo import MongoClient

def getISBN(title, author):
    """ get book isbn by use of getisbnBydouban and getisbnByamazon module"""
    isbn = ''
    isbn = getisbnBydouban.getISBN(title, author)

    if (isbn==''):
        asin = getisbnByamazon.getASIN(title, author)
        isbn = getisbnByamazon.getISBN(asin)
    else:
        return isbn
    return isbn

def findNoisbn(title, author, spider='Shaishufang'):
    """ find no isbn book in Shaishufang and getISBN. """
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

    curcnt = cur.count()
    if (curcnt==1):
        try:
            isbn = cur[0]['data']['ISBN']
        except:
            isbn = getISBN(title, author)
        return isbn

def test(title, author):
    if (title !='') and (author != ''):
        #isbn = getISBN(title, author)
        isbn = findNoisbn(title, author)
        print title, author, isbn

if (__name__=='__main__'):
    #豆瓣
    title = '汉书集释（全十二册）'
    author = '施之勉'
    #亚马逊
    #title = '上海私人地圖'
    #author = '周佩紅'
    test(title, author)
