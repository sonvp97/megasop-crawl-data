import scrapy
from bs4 import BeautifulSoup

from database import get_links_from_guardian
from items import SaveToDBGuardian


class LinkSpider(scrapy.Spider):
    name = 'link-guardian'

    def start_requests(self):
        links = get_links_from_guardian()
        for link in links:
            yield scrapy.Request(url=link, callback=self.parse)

    def parse(self, response, **kwargs):
        if response.status != 200:
            self.log(f"Lỗi {response.status} khi truy cập link {response.url}")
            return

        html_content = response.body
        soup = BeautifulSoup(html_content, "html.parser")

        div_element_name = soup.find("div", class_="product-title")
        if div_element_name:
            product_name = div_element_name.find("h1").text.strip()
        else:
            product_name = None

        span_element_price = soup.find("span", class_="pro-price")
        if span_element_price:
            product_price = span_element_price.text.strip().replace(",", "").replace("₫", "")
        else:
            product_price = None

        button_element = soup.find("button", class_="add-to-cartProduct")
        if button_element and button_element.has_attr("disabled"):
            product_status = "Hết hàng"
        else:
            product_status = "Còn hàng"


        item = SaveToDBGuardian()
        item['name'] = product_name
        item['price'] = product_price
        item['status'] = product_status
        item['table_name'] = 'guardian'
        yield item
