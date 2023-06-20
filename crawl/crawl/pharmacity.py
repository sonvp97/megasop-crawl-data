import scrapy
from database import get_links_from_pharmacity
from items import SaveToDBPharmacity



class SaveToDB(scrapy.Item):
    name = scrapy.Field()
    price = scrapy.Field()
    total = scrapy.Field()
    brick_price = scrapy.Field()
    table_name = scrapy.Field()

class LinkPharmacity(scrapy.Spider):
    name = 'link-pharmacity'

    def start_requests(self):
        proxy_url = "http://ufqvwswy:878q43xw34ks@154.95.36.199:6893"
        links = get_links_from_pharmacity()
        for link in links:
            url = 'https://api-gateway.pharmacity.vn/api/product?slug=' + link
            yield scrapy.Request(url, callback=self.parse_product, headers={'User-Agent': 'Mozilla/5.0'}, meta={'proxy': proxy_url})

    def parse_product(self, response):
        print(response.meta.get('proxy'))
        if response.status == 200:

            data = response.json()
            products = data['data']['product']

            product_name = products['name']
            product_price = products['pricing']['priceRange']['start']['gross']['amount']
            total_quantity = products['variants'][0]['quantityAvailable']
            brick_price = products['pricing']['priceRangeUndiscounted']['start']['gross']['amount']

            item = SaveToDB()
            item['name'] = product_name
            item['price'] = product_price
            item['total'] = total_quantity
            item['brick_price'] = brick_price
            item['table_name'] = 'pharmacity'
            yield item
        else:
            self.logger.error('Yêu cầu không thành công. Mã lỗi: %s', response.status)


