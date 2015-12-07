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

def test(title, author):
    if (title !='') and (author != ''):
        isbn = getISBN(title, author)
        print title, author, isbn

if (__name__=='__main__'):
    #豆瓣
    # title = '汉书集释（全十二册）'
    # author = '施之勉'
    #亚马逊
    #title = '上海私人地圖'
    #author = '周佩紅'
    title = '白夜行'
    author = '作者:（日）东野圭吾 著，刘姿君 译'
    test(title, author)
