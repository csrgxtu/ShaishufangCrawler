# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy

# 用户的meta信息
class UserItem(scrapy.Item):
    UID = scrapy.Field()
    UserName = scrapy.Field()
    TotalBooks = scrapy.Field()
    TotalPages = scrapy.Field()

# 书籍的meta信息
class BookItem(scrapy.Item):
    UID = scrapy.Field()
    UBID = scrapy.Field()
    BookName = scrapy.Field()
    Author = scrapy.Field()
    Publisher = scrapy.Field()
    PubTime = scrapy.Field()
    ISBN = scrapy.Field()
    Abstract = scrapy.Field()
