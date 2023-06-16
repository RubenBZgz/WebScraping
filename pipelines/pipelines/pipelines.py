# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from scrapy.exporters import JsonItemExporter


class SaveJsonPipeline:
    def process_item(self, item, spider):
       filename = item['filename']
       del item['filename']
       JsonItemExporter(open(filename, "wb")).export_item(item)
       return item