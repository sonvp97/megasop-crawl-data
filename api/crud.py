import urllib.parse
import aiohttp

from bs4 import BeautifulSoup
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, exists
from fastapi import HTTPException
import requests

from database import SessionLocal
from models import Guardian, GuardianLink, Hasaki, HasakiLink, Watson, WatsonLink

import models
import schemas


def get_all_guardian_crud(db: Session):
    return db.query(Guardian).all()

async def get_data_guardian_crud(keyWord: str):
    session = aiohttp.ClientSession()
    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (HTML, like Gecko) Chrome/105.0.0.0 Safari/537.36'
    }
    encode_string = urllib.parse.quote(keyWord)
    url = f"https://www.guardian.com.vn/search?type=product&q=filter=((title%3Aproduct%20contains%20{encode_string})%7C%7C(titlespace%3Aproduct%3D*{encode_string})%7C%7C(sku%3Aproduct%20contains%20{encode_string}))&sortby=(sold_quantity:product=desc)"

    async with session.get(url, headers=headers) as resp:
        if resp.status != 200:
            return {"error": f"bad status code {resp.status}"}

        soup = BeautifulSoup(await resp.text(), "html.parser")
        product_list = []
        product_elements = soup.find_all("div", class_="col-md-3 col-sm-6 col-xs-6 pro-loop")
        id = 0
        for product_element in product_elements:
            product_info = {"name": product_element.find("h3", class_="pro-name").text.strip()}
            product_info["id"] = id
            id += 1
            price_element = product_element.find("span", class_="p-compare")
            if price_element:
                product_info["price"] = price_element.text.strip().replace(",", "").replace("₫", "")
            else:
                product_info["price"] = None
            link_element = product_element.find("a")
            if link_element:
                href = link_element.get('href')
                product_info["link"] = "https://www.guardian.com.vn" + href
            else:
                product_info["link"] = None
            product_list.append(product_info)

    await session.close()

    return product_list


def save_guardian_links_crud(s_link_list: schemas.SLinkList):
    session = SessionLocal()
    current_count = session.query(GuardianLink).count()
    remaining_capacity = 1001 - current_count
    saved_links = []
    for s_link in s_link_list.s_links:
        existing_link = session.query(exists().where(GuardianLink.link == s_link)).scalar()
        if not existing_link and remaining_capacity > 0:
            new_guardian_link = GuardianLink(link=s_link)
            saved_links.append(new_guardian_link)
            remaining_capacity -= 1
    session.add_all(saved_links)
    session.commit()
    session.close()
    if remaining_capacity <= 0:
        return {"message": "limit_exceeded"}
    else:
        return {"message": "successful"}

# ____________________________________________________________________________
def get_all_hasaki_crud(db: Session):
    return db.query(Hasaki).all()

async def get_data_hasaki_crud(keyWord: str):
    session = aiohttp.ClientSession()
    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (HTML, like Gecko) Chrome/105.0.0.0 Safari/537.36'
    }
    encode_string = urllib.parse.quote(keyWord)
    url = f"https://hasaki.vn/catalogsearch/result/?q={encode_string}"

    async with session.get(url, headers=headers) as resp:
        if resp.status != 200:
            return {"error": f"bad status code {resp.status}"}

        soup = BeautifulSoup(await resp.text(), "html.parser")
        product_list = []
        product_elements = soup.find_all("div", class_="item_list_cate")
        id = 0
        for product_element in product_elements:
            product_info = {"name": product_element.find("div", class_="vn_names").text.strip()}
            product_info["id"] = id
            id += 1
            brand_element = product_element.find("div", class_="width_common txt_color_1 space_bottom_3")
            if brand_element:
                product_info["brand_name"] = brand_element.text.strip()
            else:
                product_info["brand_name"] = None

            price_element = product_element.find("strong", class_="item_giamoi")
            if price_element:
                product_info["price"] = price_element.text.strip().replace(" ", "").replace("₫", "").replace(".", "")
            else:
                product_info["price"] = None

            quantity_element = product_element.find("span", class_="item_count_by")
            if quantity_element:
                product_info["quantity"] = quantity_element.text.strip()
            else:
                product_info["quantity"] = None

            link_element = product_element.find("a", class_="block_info_item_sp width_common")
            if link_element:
                href = link_element.get('href')
                product_info["link"] = href
            else:
                product_info["link"] = None

            product_list.append(product_info)

    await session.close()

    return product_list

def save_hasaki_links_crud(s_links: schemas.SLinkList, db: Session):
    try:
        for s_link in s_links.s_links:
            new_s_link = HasakiLink(link=s_link)
            db.add(new_s_link)
        db.commit()
        return "successful"
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        db.close()

# watsons____________________________________________________________________

def get_all_watsons_crud(db: Session):
    return db.query(Watson).all()

def get_data_watsons_crud(keyWord: str):
    session = requests.Session()
    session.headers.update({
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (HTML, like Gecko) Chrome/105.0.0.0 '
                      'Safari/537.36'
    })
    encode_string = urllib.parse.quote(keyWord)
    res = f"https://www.watsons.vn/vi/search?text={encode_string}"
    resp = session.get(res)
    if resp.status_code != 200:
        return {"error": f"bad status code {resp.status_code}"}


    soup = BeautifulSoup(resp.content, "html.parser")
    element = soup.find_all('e2-product-tile', class_='ng-star-inserted')

    product_list = []
    id = 1

    for item in element:
        product_info = {"id": id}
        id += 1

        name_element = item.find('h2', class_='productName')
        if name_element:
            product_info["name"] = name_element.text.strip()
        else:
            product_info["name"] = None

        price_element = item.find('div', class_='productPrice')
        if price_element:
            price = price_element.text.strip().split()[0].replace('.', '').replace('₫', '')
            product_info["price"] = price
        else:
            product_info["price"] = None

        link_element = item.find('a', class_='ClickSearchResultEvent_Class gtmAlink')
        if link_element:
            product_info["link"] ="https://www.watsons.vn/" + link_element['href']
            print(product_info)
        else:
            product_info["link"] = None

        product_list.append(product_info)

    return product_list

def save_watsons_links_crud(s_link_list: schemas.SLinkList, db: Session):
    try:
        for s_link in s_link_list.s_links:
            new_s_link = WatsonLink(link=s_link)
            db.add(new_s_link)
        db.commit()
        return "successful"
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        db.close()



# Pharmacity
def get_all_pharmacitys(db: Session, skip: int, limit: int):
    response = schemas.PharmacityList(
        listPharmacity=db.query(models.Pharmacity).offset(skip).limit(limit).all(),
        count=db.query(models.Pharmacity).count()
    )
    return response





def create_link_pharmacity(db: Session, s_links: schemas.SLinkList):
    reponse = schemas.Reponse(message="successful")
    links = db.query(models.PharmacityLink).all()
    size = len(links)
    if size == 1000:
        return schemas.Response(message="Failing!")
    for s_link in s_links.s_links:
        count = db.query(models.PharmacityLink).filter_by(link=s_link).count()
        if count == 0:
            db_link = models.PharmacityLink(link=s_link)
            db.add(db_link)
            db.commit()
            db.refresh(db_link)
    return reponse

def search_pharmacity(keyWord: str):
    url = 'https://api-gateway.pharmacity.vn/api/product-search'
    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (HTML, like Gecko) Chrome/105.0.0.0 Safari/537.36'
    }
    params = {
        'search': keyWord,
        'size': '50'
    }
    proxy_url = "http://ufqvwswy:878q43xw34ks@154.95.36.199:6893"
    proxies = {
        'http': proxy_url,
        'https': proxy_url
    }

    response = requests.get(url, headers=headers, params=params, proxies=proxies)
    if response.status_code == 200:
        data = response.json()
        products = data['data']['products']['edges']
        id = 0;
        processed_data = []
        for item in products:
            product_data = {
                'id': id,
                'name': item['node']['name'],
                'price': item['node']['pricing']['priceRange']['start']['gross']['amount'],
                'link': item['node']['slug'],
                'quantity': item['node']['variants'][0]['quantityAvailable'],
                'brickPrice': item['node']['pricing']['priceRangeUndiscounted']['start']['gross']['amount']
            }
            id += 1
            processed_data.append(product_data)
        return processed_data
    else:
        # Xử lý khi có lỗi xảy ra
        return None

