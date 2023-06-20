import scrapy


class SaveToDB(scrapy.Item):
    name = scrapy.Field()
    price = scrapy.Field()
    total = scrapy.Field()
    quantity = scrapy.Field()
    brand_name = scrapy.Field()

class SaveToDBPharmacity(scrapy.Item):
    name = scrapy.Field()
    price = scrapy.Field()
    total = scrapy.Field()
    table_name = scrapy.Field()
class SaveToDBGuardian(scrapy.Item):
    name = scrapy.Field()
    price = scrapy.Field()
    status = scrapy.Field()
    table_name = scrapy.Field()