
BOT_NAME = "crawl"

SPIDER_MODULES = ["crawl.spiders"]
NEWSPIDER_MODULE = "crawl.spiders"
ROBOTSTXT_OBEY = True

ITEM_PIPELINES = {
    'crawl.pipelines.MySQLPipeline': 300,
}

MYSQL_HOST = 'localhost'
MYSQL_PORT = 3306
MYSQL_DATABASE = 'scrapy'
MYSQL_USER = 'root'
MYSQL_PASSWORD = '123456'


REQUEST_FINGERPRINTER_IMPLEMENTATION = "2.7"
TWISTED_REACTOR = "twisted.internet.asyncioreactor.AsyncioSelectorReactor"
FEED_EXPORT_ENCODING = "utf-8"
