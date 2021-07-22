# Scrapy Piplines
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymysql
import logging
import json
from scrapy.exporters import JsonItemExporter

class JsonWriterPipeline(object):
    def __init__(self, **kwargs):
        from time import strftime
        self.file = open(f'./log/data_{kwargs['GALL']}_{strftime("%Y%m%d-%H%M%S")}.json', 'w')
        self.exporter = JsonItemExporter(
            self.file,
            encoding="utf-8",
            ensure_ascii=False
        )
        self.exporter.start_exporting()

    def close_spider(self, spider):
        self.exporter.finish_exporting()
        self.file.close()

    def process_item(self, item, spider):
        self.exporter.export_item(item)
        return item
