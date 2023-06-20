from pydantic import BaseModel


class HasakiLink(BaseModel):
    pass

class Hasaki(BaseModel):
    pass

class WatsonLink(BaseModel):
    pass

class Watson(BaseModel):
    pass

class Pharmacity(BaseModel):
    id: int
    name: str
    price: int
    total: int
    brick_price: int

    class Config:
        orm_mode = True

class PharmacityLink(BaseModel):
    id: int
    link: str

    class Config:
        orm_mode = True
class SLinkList(BaseModel):
    s_links: list[str]
class Reponse(BaseModel):
    message: str
class GuardianLink(BaseModel):
    pass

class Guardian(BaseModel):
    pass
class PharmacityList(BaseModel):
    listPharmacity: list[Pharmacity]
    count: int

