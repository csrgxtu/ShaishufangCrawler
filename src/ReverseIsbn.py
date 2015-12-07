#!/usr/bin/env python
# coding=utf-8
#
# Author: Archer Reilly
# Date: 07/Dec/2015
# File: ReverseIsbn.py
# Desc: reverse, get isbn according to the bookname and author
#
# Produced By BR
import getisbn
from Utility import loadMatrixFromFile, saveLstToFile
import sys

def run(uid):
    ISBNS = []

    res = loadMatrixFromFile(uid + '.csv')
    #print res[0][0], res[0][1]

    for book in res:
        title = book[0]
        author = book[1]
        isbn = getisbn.getISBN(title, author)
        if isbn != '':
            print title, author, isbn
            ISBNS.append(isbn)
        else:
            print title, author, None

        #getisbn.test(title, author)

    saveLstToFile(uid + '-isbns.csv', ISBNS)
    
    #title = res[0][0]
    #author = res[0][1]
    #title = '眼镜蛇事件'
    #author = '作者:[美]理查德·普莱斯顿 著，吴国杰，郑笑丹 译'
    #getisbn.test(title, author)

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print 'Usage: python ReverseIsbn.py uid'
    else:
        run(sys.argv[1])
