from typing import Optional

from pydantic import BaseModel
from datetime import datetime


class Hasaki(BaseModel):
    id: int
    name: str
    price: int
    total: str
    original_price: int
    crawl_time: datetime

    class Config:
        orm_mode = True


class ReportRequest(BaseModel):
    fromDate: datetime
    toDate: datetime


class Report(BaseModel):
    id: int
    brand_id: int
    report_id: str
    success: int
    failure: int
    total: int
    start_crawl: datetime
    end_crawl: datetime

    class Config:
        orm_mode = True


class ReportDetail(BaseModel):
    id: int
    name: str
    status: int
    time: datetime


class WatsonLink(BaseModel):
    link: str
    id_watson: int


class CronRequest(BaseModel):
    name: str
    quantity: int
    unit: str
    status: int


class CheckToken(BaseModel):
    token: Optional[str]


class ReportID(BaseModel):
    reportID: str


class Watson(BaseModel):
    id: int
    name: str
    price: int
    total: int
    original_price: int
    crawl_time: datetime

    class Config:
        orm_mode = True


class Pharmacity(BaseModel):
    id: int
    name: str
    price: int
    total: int
    original_price: int
    crawl_time: datetime

    class Config:
        orm_mode = True


class PharmacityLink(BaseModel):
    id: int
    link: str

    class Config:
        orm_mode = True


class SaveLink(BaseModel):
    name: str
    link: str


class SLinkList(BaseModel):
    s_links: list[SaveLink]
    id_brand: int

    def __getitem__(self, item):
        return getattr(self, item)


class SLinkListWatson(BaseModel):
    s_links: list[WatsonLink]


class Response(BaseModel):
    message: str
    size: int


class GuardianLink(BaseModel):
    pass


class Guardian(BaseModel):
    id: int
    name: str
    price: int
    status: str
    original_price: int
    crawl_time: datetime

    class Config:
        orm_mode = True


class PharmacityList(BaseModel):
    listPharmacity: list[Pharmacity]
    count: int


class HasakiList(BaseModel):
    listHasaki: list[Hasaki]
    count: int


class GuardianList(BaseModel):
    listGuardian: list[Guardian]
    count: int


class WatsonList(BaseModel):
    listWatson: list[Watson]
    count: int


class ReportList(BaseModel):
    listReport: list[Report]
    count: int


class ReportDetailList(BaseModel):
    listReportDetail: list[ReportDetail]
    count: int


# Login ___________________________________________________________________________
class LoginRequest(BaseModel):
    username: str
    password: str


class TokenCheck(BaseModel):
    token: str


class Setting(BaseModel):
    name: str
    quantity: int
    unit: str
    status: str
