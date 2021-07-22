# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class IdoldcItem(scrapy.Item):
    # parse
    gall_count = scrapy.Field()
    gall_recommend = scrapy.Field()
    post_id = scrapy.Field()
    post_type = scrapy.Field()
    reply_num = scrapy.Field()
    title = scrapy.Field()
    uploaded_date = scrapy.Field()
    url = scrapy.Field()
    userid= scrapy.Field()
    userip = scrapy.Field()
    usernick = scrapy.Field()
    gallery = scrapy.Field()
    referer = scrapy.Field()
    gall_type=scrapy.Field()
    error = scrapy.Field()
