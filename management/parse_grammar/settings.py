# -*- coding: utf-8 -*-

BOT_NAME = 'gramma-parser'

SPIDER_MODULES = ['gramma-parser.spiders']
NEWSPIDER_MODULE = 'gramma-parser.spiders'

ITEM_PIPELINES = {
    'gramma-parser.pipelines.MongoPipeline': 300,
}
MONGO_URI = 'mongodb://46.101.216.92'
MONGO_DATABASE = 'enclever_test'

