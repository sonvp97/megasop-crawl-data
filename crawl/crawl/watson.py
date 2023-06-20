import scrapy
from database import get_links_from_watson

from bs4 import BeautifulSoup

class SaveToDB(scrapy.Item):
    name = scrapy.Field()
    price = scrapy.Field()
    total = scrapy.Field()
    table_name = scrapy.Field()

class LinkWatson(scrapy.Spider):
    name = 'watson-spider'

    def start_requests(self):
        links = get_links_from_watson()
        for link in links:
            yield scrapy.Request(url=link, callback=self.parse)

    def parse(self, response, **kwargs):
        html_content = response.body
        soup = BeautifulSoup(html_content, "html.parser")
        elements = soup.find('e2-product-summary', class_='ng-star-inserted')
        
        element_name = elements.find('div','title-name ng-star-inserted').text.strip()

        element_price = elements.find('div','displayPrice ng-star-inserted').text.strip().replace("₫", "").replace(".", "")

        item = SaveToDB()
        item['name'] = element_name = elements.find('div','title-name ng-star-inserted').text.strip()

        item['price'] = element_price = elements.find('div','displayPrice ng-star-inserted').text.strip().replace("₫", "").replace(".", "")

        item['total'] = None
        item['table_name'] = 'watson'
        yield item
    