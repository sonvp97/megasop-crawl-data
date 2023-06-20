# Megasop-BOT crawl demo : https://hasaki.vn/

****
    Megasop-BOT
    |_____api
    |_____crawl
    |_____myenv
    |_____script_database
    |Readme.md
****
https://ibb.co/5YcrVRp

Import script to create database.

### Use Command prompt from: megasop-crawl-data
```bash
python -m venv myenv
```
***
### B1 :  cmd from megasop-crawl-data : 
```bash
myenv\Scripts\activate
```
```bash
pip install uvicorn
```
```bash
pip install fastapi
```
```bash
pip install scrapy
```
```bash
pip install requests
```
```bash
pip install schedule
```
```bash
pip install beautifulsoup4
```
```bash
pip install aiohttp
```
```bash
pip install sqlalchemy
```
```bash
pip install mysql-connector-python
```
```bash
pip install mysqlclient
```

### B2 : Start API : 
```bash
cd .\api\ 
```
```bash
uvicorn main:app --reload 
```


- swagger API : http://127.0.0.1:8000/docs#/
***
### API Get_Data:
    - input any keyword. Example :"nuoc hoa nam" or "nước hoa"
    - Reponse : A product list have more info : name , price , brand_name , link
    - Copy link or more link to API Save_Link
***

### API Save_Link :
  - Past link copy from reponse API Get_Data and submit

***

### B3: Start auto crwal after 1 one minutes
```bash
cd .\crawl\crawl\ 
```
```bash
python run.py
```

View database