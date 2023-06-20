import urllib
from idlelib.query import Query

from bs4 import BeautifulSoup
from starlette.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from fastapi import Depends, FastAPI, HTTPException
from database import SessionLocal, engine
from schemas import SLinkList

import database
import crud
import models
import schemas
models.Base.metadata.create_all(bind=engine)

app = FastAPI()
origins = [
    "http://localhost",
    "http://localhost:8080",
    "http://localhost:3000"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/guardian")
def get_all_guardian(db: Session = Depends(get_db)):
    result = crud.get_all_guardian_crud(db)
    return result

@app.get("/guardian/{keyWord}")
async def get_data_guardian(keyWord: str):
    return await crud.get_data_guardian_crud(keyWord)

@app.post("/guardian/save")
def save_guardian_links(s_link_list: SLinkList):
    return crud.save_guardian_links_crud(s_link_list)

# ___________________________________________________________

@app.get("/hasaki")
def get_all_hasaki(db: Session = Depends(get_db)):
    result = crud.get_all_hasaki_crud(db)
    return result

@app.get("/hasaki/{keyWord}")
async def get_data_hasaki(keyWord: str):
    return await crud.get_data_hasaki_crud(keyWord)

@app.post("/hasaki/save")
def save_hasaki_links(s_links: SLinkList,db: Session = Depends(get_db) ):
    return crud.save_hasaki_links_crud(s_links = s_links, db=db)
# ___________________________________________________________

@app.get("/watsons")
def get_all_watsons(db: Session = Depends(get_db)):
    result = crud.get_all_watsons_crud(db)
    return result

@app.get("/watsons/{keyWord}")
def get_data_watsons(keyWord: str):
    return crud.get_data_watsons_crud(keyWord)

@app.post("/watsons/save")
def save_watsons_links(s_link_list: SLinkList, db: Session = Depends(get_db)):
    return crud.save_watsons_links_crud(s_link_list=s_link_list, db=db)
# @app.post("/watsons/save", response_model=list[schemas.SLinkList])
# async def save_s_links(s_links: schemas.SLinkList, db: Session = Depends(get_db)):
#     for s_link in s_links.s_links:
#         return crud.create_link_watson(db, s_link)
# ___________________________________________________________

@app.get("/pharmacity/")
def get_all_pharmacity(
    skip: int,
    limit: int,
    db: Session = Depends(get_db)
):
    return crud.get_all_pharmacitys(db = db, skip=skip, limit=limit)

@app.post("/linkPharmacity/", response_model= schemas.Reponse)
async def create_link_pharmacity(s_links: schemas.SLinkList, db: Session = Depends(get_db)):
    return crud.create_link_pharmacity(s_links=s_links, db=db)

@app.get("/pharmacity/{keyWord}")
def search_pharmacity(keyWord: str):
    return crud.search_pharmacity(keyWord)

