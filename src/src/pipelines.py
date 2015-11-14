# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymongo
from scrapy.conf import settings
from scrapy.exceptions import DropItem
import logging

class MongoDBPipeline(object):
    def __init__(self):
        connection = pymongo.MongoClient(
            settings['MONGODB_SERVER'],
            settings['MONGODB_PORT']
        )
        db = connection[settings['MONGODB_DB']]
        self.usersCollection = db[settings['MONGODB_USERS_COLLECTION']]
        self.booksCollection = db[settings['MONGODB_BOOKS_COLLECTION']]

    def process_item(self, item, spider):
        logging.info(spider.userOrBook)
        valid = True
        for data in item:
            if not data:
                valid = False
                raise DropItem("Missing {0}!".format(data))

        if valid:
            if spider.userOrBook == 'User':
                self.usersCollection.insert(dict(item))
                logging.info("User added to MongoDB database")
            elif spider.userOrBook == 'Book':
                self.booksCollection.insert(dict(item))
                logging.info("Book added to MongoDB database")
            else:
                pass

            # if item['UBID']:
            #     self.booksCollection.insert(dict(item))
            #     logging.info("Book added to MongoDB database")
            # else:
            #     self.usersCollection.insert(dict(item))
            #     logging.info("User added to MongoDB database")

        return item

class SrcPipeline(object):
    def process_item(self, item, spider):
        return item
