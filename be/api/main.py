import subprocess
from datetime import datetime
from typing import Optional

import jwt
from croniter import croniter
from crontab import CronTab
from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session
from starlette.middleware.cors import CORSMiddleware

import config
import crud
import models
import schemas
from database import SessionLocal, engine
from security import verify_password, generate_token, validate_token, check_token_expired

models.Base.metadata.create_all(bind=engine)

app = FastAPI()
origins = [
    "http://localhost",
    "http://localhost:8080",
    "http://localhost:3000",
    "https://reactjs-megasop.vercel.app",
    "https://react.thanhdev.info"
]

SECURITY_ALGORITHM = 'HS256'
SECRET_KEY = '123456'

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/cron-job", dependencies=[Depends(validate_token)])
def cron_tab_control(request: schemas.Setting, db: Session = Depends(get_db)):
    shop_cron = CronTab(user=config.USER_ROOT)
    path = config.PATH_FILE_CRAWL + "run.py"

    shop_cron.remove_all()
    job = shop_cron.new(command=f"python3 {path}", comment='megasop')
    if request.name != 'cronjob':
        return {
            'status': "failed",
            'message': 'name mặc định nhập cronjob'
        }
    if request.status == "true":
        if request.quantity:
            if request.unit == 'hour':
                job.setall(f"0 */{request.quantity} * * *")
                print('hour')
            elif request.unit == 'minute':
                job.setall(f"*/{request.quantity} * * * *")
                print('minute')
            else:
                return {
                    'status': "failed",
                    'message': 'unit nhập hour hoặc minute '
                }
            result = crud.save_setting_cron_job(db=db, setting=request)
        else:
            return {
                'status': "failed",
                'message': 'quantity nhập số không để trống'
            }
        shop_cron.write()
        return {
            'status': 'success',
            'cronjob': {
                'name': result[0]['name'],
                'quantity': result[0]['quantity'],
                'unit': result[0]['unit'],
                'status': result[0]['status']
            }
        }
    elif request.status == 'false':
        job.enable(request.status)
        subprocess.call(['/usr/bin/crontab', '-r'])
        crud.save_setting_cron_job(db=db, setting=request)
        print("delete")
        return {
            'status': 'success',
            'massage': 'đã xoá lịch'
        }
    else:
        return {
            'status': "failed",
            'message': 'trạng thái status nhập true hoặc false '
        }


@app.get("/job-exist", dependencies=[Depends(validate_token)])
def get_job_exist(db: Session = Depends(get_db)):
    name = 'cronjob'
    comment = "megasop"
    shop_cron = CronTab(user="root")

    for job in shop_cron:
        if job.comment == comment:
            base = datetime.now()
            job_str = str(job)
            comment_index = job_str.find(" py")
            cron_only = job_str[:comment_index].strip()

            time = croniter(cron_only, base)
            result = crud.get_setting_config_by_name(db, name)
            time_next = time.get_next(datetime).strftime("%Y-%m-%d %H:%M:%S")
            return {
                'status': 'success',
                'message': 'on',
                'cronjob': result,
                'next_time': time_next
            }
    return{
        'status': "success",
        'message': 'off'
        }

@app.get("/guardian", dependencies=[Depends(validate_token)])
def get_all_guardian(
        skip: int,
        limit: int,
        name: str,
        db: Session = Depends(get_db)
):
    return crud.get_all_guardian(db=db, skip=skip, limit=limit, name=name)


@app.get("/guardian/{keyWord}", dependencies=[Depends(validate_token)])
async def search_guardian(keyWord: str):
    return await crud.crawl_guardian(keyWord)


@app.get("/hasaki", dependencies=[Depends(validate_token)])
def get_all_hasaki(
        skip: int,
        limit: int,
        name: str,
        db: Session = Depends(get_db)
):
    return crud.get_all_hasaki(db=db, skip=skip, limit=limit, name=name)


@app.get("/hasaki/{keyWord}", dependencies=[Depends(validate_token)])
async def search_hasaki(keyWord: str):
    return await crud.crawl_hasaki(keyWord)


@app.get("/watsons", dependencies=[Depends(validate_token)])
def get_all_watsons(
        skip: int,
        limit: int,
        name: str,
        db: Session = Depends(get_db)
):
    return crud.get_all_watsons(db=db, skip=skip, limit=limit, name=name)


@app.get("/watsons/{keyWord}", dependencies=[Depends(validate_token)])
def search_watsons(keyWord: str):
    return crud.crawl_watsons(keyWord)


def get_all_pharmacity(
        skip: int,
        limit: int,
        name: str,
        db: Session = Depends(get_db)
):
    return crud.get_all_pharmacitys(db=db, skip=skip, limit=limit, name=name)


@app.post("/link", dependencies=[Depends(validate_token)])
async def create_link(s_links: schemas.SLinkList, db: Session = Depends(get_db)):
    return crud.create_link(db=db, s_links=s_links)


@app.get("/pharmacity/{keyWord}", dependencies=[Depends(validate_token)])
def search_pharmacity(keyWord: str):
    return crud.search_pharmacity(keyWord)


@app.get("/pharmacity", dependencies=[Depends(validate_token)])
def get_all_pharmacity(
        skip: int,
        limit: int,
        name: str,
        db: Session = Depends(get_db)
):
    return crud.get_all_pharmacitys(db=db, skip=skip, limit=limit, name=name)


@app.get("/report", dependencies=[Depends(validate_token)])
def get_report(
        from_date: datetime,
        to_date: datetime,
        skip: int,
        limit: int,
        brand_id: Optional[int] = None,
        db: Session = Depends(get_db)):
    return crud.get_all_report(db, from_date, to_date, skip, limit, brand_id)


@app.post('/login')
def login(request_data: schemas.LoginRequest, db: Session = Depends(get_db)):
    print(f'[x] request_data: {request_data.__dict__}')
    if verify_password(username=request_data.username, password=request_data.password, db=db):
        token = generate_token(request_data.username)
        payload = jwt.decode(token, SECRET_KEY, algorithms=[SECURITY_ALGORITHM])
        expiration_time = datetime.fromtimestamp(payload["exp"])
        return {
            'token': token,
            'expiration_time': expiration_time
        }
    else:
        raise HTTPException(status_code=404, detail="User not found")


@app.post('/expired/')
def check_token_expire(check_token: schemas.CheckToken):
    return check_token_expired(check_token.token)


@app.get('/report/detail', dependencies=[Depends(validate_token)])
def get_report_detail_by_report_id(
        skip: int,
        limit: int,
        report_id: str,
        brand_id: int,
        status: Optional[str] = None,
        db: Session = Depends(get_db)):
    return crud.get_detail_report_by_report_id(db, skip, limit, report_id, brand_id, status)
