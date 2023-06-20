import scrapy
from bs4 import BeautifulSoup

from database import get_links_from_database
from database import get_links_from_pharmacity
from items import SaveToDB


class SaveToDB(scrapy.Item):
    name = scrapy.Field()
    price = scrapy.Field()
    total = scrapy.Field()
    status = scrapy.Field()
    table_name = scrapy.Field()


class LinkSpider(scrapy.Spider):
    name = 'link-spider'

    def start_requests(self):
        proxy_url = "http://ufqvwswy:878q43xw34ks@154.95.36.199:6893"
        links = get_links_from_database()
        count = len(links)
        print(count)
        for link in links:
            yield scrapy.Request(url=link, callback=self.parse, meta={'proxy': proxy_url})

    def parse(self, response, **kwargs):
        if response.status != 200:
            self.log(f"Lỗi {response.status} khi truy cập link {response.url}")
            return

        html_content = response.body
        soup = BeautifulSoup(html_content, "html.parser")
        span_element_name = soup.find('span', class_='product__title', itemprop="name")
        product_name = span_element_name.text.strip()
        print(product_name)
        span_element_price = soup.find('span', class_='txt_price')
        product_price = span_element_price.text.strip().replace("₫", "").replace(".", "")

        txt_color_2_elements = soup.find_all('span', class_='txt_color_2')
        numbers = [element.text.strip() for element in txt_color_2_elements]

        positive_numbers = []
        for num in numbers:
            if num.isdigit():
                integer_num = int(num)
                if integer_num > 0:
                    positive_numbers.append(integer_num)
        total_store = sum(positive_numbers)

        # print(soup.find('div', class_='button_check_stock_card').find("b").text.strip())

        div = soup.find('div', class_='button_check_stock_card')
        if div:
            b = div.find("b").text.strip()
            if b[0] != '0':
                product_status = 'Còn hàng'
            else:
                product_status = 'Hết hàng'
            print(product_status)
        else:
            print('Không tìm thấy thông tin trạng thái sản phẩm')

        item = SaveToDB()
        item['name'] = product_name
        item['price'] = product_price
        item['total'] = total_store
        item['status'] = product_status
        item['table_name'] = 'hasaki'
        yield item
