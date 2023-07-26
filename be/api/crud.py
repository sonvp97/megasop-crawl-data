import urllib.parse
from datetime import datetime

import aiohttp
import requests
from bs4 import BeautifulSoup
from sqlalchemy import desc
from sqlalchemy.orm import Session

import config
import models
import schemas


def get_all_guardian(db: Session, skip: int, limit: int, name: str = None):
    try:
        query = db.query(models.ProductList).filter(
            (models.ProductList.brand_id == 3) & (models.ProductList.status == 1)
        )

        if name is not None and name != "undefined":
            query = query.filter(models.ProductList.name.ilike(f"%{name.replace(' ', '%')}%"))
        query = query.order_by(desc(models.ProductList.crawl_time))
        counter = skip + 1
        results = []

        for object in query.offset(skip).limit(limit).all():
            objectDto = {
                'id': counter,
                'name': object.name,
                'price': object.price,
                'status': object.total if object.total else "",
                'original_price': object.original_price,
                'crawl_time': object.crawl_time
            }
            counter += 1
            results.append(objectDto)
        response = schemas.GuardianList(
            listGuardian=results,
            count=query.count()
        )
        return response
    except Exception as e:
        return {
            'status': 'failed',
            'message': str(e)
        }
    finally:
        db.close()


async def crawl_guardian(keyWord: str):
    product_list = []
    id = 1
    for i in range(1, 5):
        session = aiohttp.ClientSession()
        headers = {
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (HTML, like Gecko) Chrome/105.0.0.0 Safari/537.36'
        }
        encode_string = urllib.parse.quote(keyWord)
        url = f"https://www.guardian.com.vn/search?type=product&q=filter=((title%3Aproduct%20contains%20{encode_string})%7C%7C(titlespace%3Aproduct%3D*{encode_string})%7C%7C(sku%3Aproduct%20contains%20{encode_string}))&sortby=(sold_quantity:product=desc)&page={i}"

        proxy_url = f"http://{config.PROXY_USER}:{config.PROXY_PASS}@{config.PROXY_IP}:{config.PROXY_PORT}"

        try:
            async with session.get(url, headers=headers, proxy=proxy_url) as resp:
            # async with session.get(url, headers=headers) as resp:

                if resp.status != 200:
                    return {"error": f"bad status code {resp.status}"}

                soup = BeautifulSoup(await resp.text(), "html.parser")

                product_elements = soup.find_all("div", class_="col-md-3 col-sm-6 col-xs-6 pro-loop")
                for product_element in product_elements:
                    product_info = {"stt": id}
                    id += 1

                    name_element = product_element.find("h3", class_="pro-name")
                    if name_element:
                        product_info["name"] = name_element.text.strip()
                    else:
                        product_info["name"] = None
                    price_element = product_element.find("span", class_="p-compare")
                    if price_element:
                        product_info["price"] = price_element.text.strip().replace(",", "").replace("₫", "")
                    else:
                        product_info["price"] = None
                    link_element = product_element.find("a")
                    if link_element:
                        href = link_element.get('href')
                        product_info["link"] = "https://www.guardian.com.vn" + href
                        product_info["id"] = href
                    else:
                        product_info["link"] = None
                    product_list.append(product_info)


        except aiohttp.ClientError as e:
            return e
        finally:
            await session.close()
    return product_list


def get_all_hasaki(db: Session, skip: int, limit: int, name: str = None):
    try:
        query = db.query(models.ProductList).filter(
            (models.ProductList.brand_id == 1) & (models.ProductList.status == 1)
        )
        if name is not None and name != "undefined":
            query = query.filter(models.ProductList.name.ilike(f"%{name.replace(' ', '%')}%"))

        query = query.order_by(desc(models.ProductList.crawl_time))

        counter = skip + 1
        results = []

        for object in query.offset(skip).limit(limit).all():
            objectDto = {
                'id': counter,
                'name': object.name,
                'price': object.price,
                'total': object.total if object.total else "",
                'original_price': object.original_price if object.original_price is not None else 0,
                'crawl_time': object.crawl_time
            }
            counter += 1

            results.append(objectDto)
        response = schemas.HasakiList(
            listHasaki=results,
            count=query.count()
        )
        return response
    except Exception as e:
        return {
            'status': 'failed',
            'message': str(e)
        }
    finally:
        db.close()


#
#
async def crawl_hasaki(keyWord: str):
    session = aiohttp.ClientSession()
    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (HTML, like Gecko) Chrome/105.0.0.0 '
                      'Safari/537.36'
    }
    encode_string = urllib.parse.quote(keyWord)
    url = f"https://hasaki.vn/catalogsearch/result/?q={encode_string}"

    proxy_url = f"http://{config.PROXY_USER}:{config.PROXY_PASS}@{config.PROXY_IP}:{config.PROXY_PORT}"

    try:
        async with session.get(url, headers=headers, proxy=proxy_url) as resp:
        # async with session.get(url, headers=headers) as resp:

            if resp.status != 200:
                return {"error": f"bad status code {resp.status}"}

            soup = BeautifulSoup(await resp.text(), "html.parser")
            product_list = []
            product_elements = soup.find_all("div", class_="item_list_cate")
            id = 1
            for product_element in product_elements:
                product_info = {"stt": id}
                id += 1
                name_element = product_element.find("div", class_="vn_names")
                if name_element:
                    product_info["name"] = name_element.text.strip()
                else:
                    product_info["name"] = None
                brand_element = product_element.find("div", class_="width_common txt_color_1 space_bottom_3")
                if brand_element:
                    product_info["brand_name"] = brand_element.text.strip()
                else:
                    product_info["brand_name"] = None

                price_element = product_element.find("strong", class_="item_giamoi")
                if price_element:
                    product_info["price"] = price_element.text.strip().replace(" ", "").replace("₫", "").replace(".",
                                                                                                                 "")
                else:
                    product_info["price"] = None

                quantity_element = product_element.find("span", class_="item_count_by")
                if quantity_element:
                    quantity = quantity_element.text.strip()
                    quantity = quantity.replace('.', '')
                    try:
                        quantity = int(quantity)
                    except ValueError:
                        quantity = None
                else:
                    quantity = None

                product_info["quantity"] = quantity

                link_element = product_element.find("a", class_="block_info_item_sp width_common")
                if link_element:
                    href = link_element.get('href')
                    product_info["link"] = href
                    product_info["id"] = href
                else:
                    product_info["link"] = None

                product_list.append(product_info)

        return product_list
    except aiohttp.ClientError as e:
        return e
    finally:
        await session.close()


def get_all_report(db: Session, from_date, to_date, skip, limit, brand_id):
    try:
        from_date = datetime.combine(from_date.date(), datetime.min.time())
        to_date = datetime.combine(to_date.date(), datetime.max.time())
        query = db.query(models.Report).filter(models.Report.end_crawl.between(from_date, to_date))
        if brand_id:
            query = query.filter(models.Report.brand_id == brand_id)

        query = query.order_by(desc(models.Report.end_crawl))
        id = skip
        result = []

        for report in query.offset(skip).limit(limit).all():
            id += 1
            reportDto = {
                'id': id,
                'brand_id': report.brand_id,
                'report_id': report.report_id,
                'success': report.success,
                'failure': report.failure,
                'total': report.total,
                'start_crawl': report.start_crawl.strftime("%Y-%m-%d %H:%M:%S"),
                'end_crawl': report.end_crawl.strftime("%Y-%m-%d %H:%M:%S")
            }
            result.append(reportDto)
        # count = query.count()
        return schemas.ReportList(
            listReport=result,
            count=query.count()
        )
    except Exception as e:
        return {
            'status': 'failed',
            'message': str(e)
        }
    finally:
        db.close()


def get_all_watsons(db: Session, skip: int, limit: int, name: str = None):
    try:
        query = db.query(models.ProductList).filter(
            (models.ProductList.brand_id == 4) & (models.ProductList.status == 1)
        )

        if name is not None and name != "undefined":
            query = query.filter(models.ProductList.name.ilike(f"%{name.replace(' ', '%')}%"))

        query = query.order_by(desc(models.ProductList.crawl_time))
        counter = skip + 1
        results = []

        for object in query.offset(skip).limit(limit).all():
            objectDto = {
                'id': counter,
                'name': object.name,
                'price': object.price,
                'total': object.total,
                'original_price': object.original_price,
                'crawl_time': object.crawl_time.strftime("%Y-%m-%d %H:%M:%S")
            }
            counter += 1
            results.append(objectDto)
        response = schemas.WatsonList(
            listWatson=results,
            count=query.count()
        )
        return response
    except Exception as e:
        return {
            'status': 'failed',
            'message': str(e)
        }
    finally:
        db.close()


#
#
def crawl_watsons(keyWord: str):
    url = "https://gb8u4czbqv-dsn.algolia.net/1/indexes/*/queries"
    headers = {
        "X-Algolia-Api-Key": "0aef964c3b68a7b11ba36b8936971de0",
        "X-Algolia-Application-Id": "GB8U4CZBQV"
    }

    proxies = {
        "http": f"http://{config.PROXY_USER}:{config.PROXY_PASS}@{config.PROXY_IP}:{config.PROXY_PORT}",
        "https": f"http://{config.PROXY_USER}:{config.PROXY_PASS}@{config.PROXY_IP}:{config.PROXY_PORT}"
    }
    keyWord = urllib.parse.quote(keyWord)
    request_body = {
        "requests": [
            {
                "indexName": "ProductPROD_WTCVN",
                "params": "clickAnalytics=true&facets=%5B%22category_lv1_vi%22%2C%22brand_vi%22%2C%22promo_vi%22%2C%22memberPrice%22%2C%22availability%22%2C%22storepickupallowed%22%2C%22xBorder%22%2C%22price_value%22%2C%22avg_rating%22%2C%22colorCode%22%2C%22subscription%22%2C%22prescription%22%2C%22refillPack%22%2C%22cleanBeauty%22%2C%22halal%22%2C%22organic%22%2C%22betterIngredients_vi%22%2C%22betterPackaging_vi%22%2C%22volume_vi%22%2C%22shopperType_vi%22%2C%22latestTrends_vi%22%5D&highlightPostTag=__%2Fais-highlight__&highlightPreTag=__ais-highlight__&hitsPerPage=50&maxValuesPerFacet=999&page=0&query=" + keyWord + "&tagFilters="
            }
        ]
    }

    product_list = []
    id = 1
    response = requests.post(url, headers=headers, json=request_body, proxies=proxies)


    data = response.json()
    watson = data["results"][0]["hits"]
    for item in watson:
        product_info = {"stt": id}
        id += 1
        product_info["id"] = item["id"]
        product_info["name"] = item["name_vi"]
        product_info["price"] = item["price_value"]
        try:
            product_info["original_price"] = item["oldprice"].split()[0].replace('.', '')
        except IndexError:
            product_info["original_price"] = None
        product_info["link"] = item["productUrl"]
        product_list.append(product_info)
    return product_list


def get_all_pharmacitys(db: Session, skip: int, limit: int, name: str = None):
    try:
        query = db.query(models.ProductList).filter(
            (models.ProductList.brand_id == 2) & (models.ProductList.status == 1)
        )

        if name is not None and name != "undefined":
            query = query.filter(models.ProductList.name.ilike(f"%{name.replace(' ', '%')}%"))

        query = query.order_by(desc(models.ProductList.crawl_time))

        counter = skip + 1
        results = []

        for pharmacity in query.offset(skip).limit(limit).all():
            pharmacity_dict = {
                'id': counter,
                'name': pharmacity.name if pharmacity.name is not None else "",
                'price': pharmacity.price if pharmacity.price is not None else "",
                'total': pharmacity.total if pharmacity.total is not None else "",
                'original_price': pharmacity.original_price if pharmacity.original_price is not None else "",
                'crawl_time': pharmacity.crawl_time if pharmacity.crawl_time is not None else ""
            }

            counter += 1
            results.append(pharmacity_dict)
        response = schemas.PharmacityList(
            listPharmacity=results,
            count=query.count()
        )
        return response
    except Exception as e:
        return {
            'status': 'failed',
            'message': str(e)
        }
    finally:
        db.close()


def create_link(db: Session, s_links: schemas.SLinkList):
    id_brand = s_links.id_brand
    try:
        links = db.query(models.Link).filter(models.Link.brand_id == id_brand)
        print(links)
        saveLinks = []
        cur_save_size = 0
        for s_link in s_links.s_links:
            count = sum(1 for link in links if link.name == s_link.name)
            if count == 0:
                cur_save_size += 1
                create_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                db_link = models.Link(name=s_link.name, create_time=create_time, brand_id=id_brand, link=s_link.link)
                saveLinks.append(db_link)
        db.add_all(saveLinks)
        db.commit()
        response = schemas.Response(message="successful", size=cur_save_size)
        return response
    except Exception as e:
        db.rollback()
        return {
            'status': 'failed',
            'message': str(e)
        }
    finally:
        db.close()


def search_pharmacity(keyWord: str):
    url = 'https://api-gateway.pharmacity.vn/api/product-search'
    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) '
                      'AppleWebKit/537.36 (HTML, like Gecko) '
                      'Chrome/105.0.0.0 Safari/537.36'
    }
    params = {
        'search': keyWord,
        'size': '50'
    }
    proxy_url = f"http://{config.PROXY_USER}:{config.PROXY_PASS}@{config.PROXY_IP}:{config.PROXY_PORT}"
    proxies = {
        'http': proxy_url,
        'https': proxy_url
    }

    response = requests.get(url, headers=headers, params=params, proxies=proxies)
    if response.status_code == 200:
        data = response.json()
        products = data['data']['products']['edges']
        id = 1
        processed_data = []
        for item in products:
            quantity = item['node']['variants'][0]['quantityAvailable']
            if quantity < 0:
                quantity = 0
            product_data = {
                'stt': id,
                'id': item['node']['id'],
                'name': item['node']['name'],
                'price': item['node']['pricing']['priceRange']['start']['gross']['amount'],
                'link': item['node']['slug'],
                'quantity': quantity,
                'originalPrice': item['node']['pricing']['priceRangeUndiscounted']['start']['gross']['amount']
            }
            id += 1
            processed_data.append(product_data)
        return processed_data
    else:
        # Xử lý khi có lỗi xảy ra
        return []


def get_setting_config_by_name(db: Session, setting_name: str):
    try:
        return db.query(models.Setting).filter(models.Setting.name == setting_name).first()
    except Exception as e:
        return {
            'status': 'failed',
            'message': str(e)
        }
    finally:
        db.close


def get_user_by_username(db: Session, username: str):
    try:
        return db.query(models.Account).filter(models.Account.username == username)
    except Exception as e:
        return {
            'status': 'failed',
            'message': str(e)
        }
    finally:
        db.close


def get_detail_report_by_report_id(db: Session, skip: int, limit: int, report_id: str, brand_id: int, status_rp: str):
    try:
        query = db.query(models.Link.link, models.ProductList.status, models.ProductList.crawl_time).join(
            models.ProductList, models.ProductList.link_id == models.Link.id).filter(
            (models.ProductList.report_id == report_id) & (models.ProductList.brand_id == brand_id))

        if status_rp != "":
            query = query.filter(models.ProductList.status == status_rp)

        query = query.order_by(desc(models.ProductList.crawl_time))

        id = skip
        result = []

        for report in query.offset(skip).limit(limit).all():
            id += 1
            reportDto = {
                'id': id,
                'name': report.link,
                'status': report.status,
                'time': report.crawl_time.strftime("%Y-%m-%d %H:%M:%S")
            }
            result.append(reportDto)
        return schemas.ReportDetailList(
            listReportDetail=result,
            count=query.count()
        )
    except Exception as e:
        return {
            'status': 'failed',
            'message': str(e)
        }
    finally:
        db.close()


def get_token(db: Session, token: str):
    try:
        result = db.query(models.Account).filter(models.Account.token == token)
        return result
    except Exception as e:
        return {
            'status': 'failed',
            'message': str(e)
        }
    finally:
        db.close()


def save_setting_cron_job(db: Session, setting: schemas.Setting):
    setting_detail = []
    try:
        setting_db = get_setting_config_by_name(db, setting.name)
        if setting_db:
            setting_db.quantity = setting.quantity
            setting_db.unit = setting.unit
            setting_db.status = 1 if setting.status == 'true' else 0
            db.commit()
            setting_detail.append({
                'name': setting.name,
                'quantity': setting.quantity,
                'unit': setting.unit,
                'status': setting.status
            })
            return setting_detail
        else:
            setting = models.Setting(
                name='crontab',
                quantity=setting.quantity,
                unit=setting.unit,
                status=setting.status)
            db.add(setting)
            db.commit()
            setting_detail.append({
                'name': setting.name,
                'quantity': setting.quantity,
                'unit': setting.unit,
                'status': setting.status
            })
            return setting_detail
    except Exception as e:
        return {
            'status': 'failed',
            'message': str(e)
        }
    finally:
        db.close()
