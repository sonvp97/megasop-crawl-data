from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()



class GuardianLink(Base):
    __tablename__ = "guardian_link"

    id = Column(Integer, primary_key=True, autoincrement=True)
    link = Column(String)

class Guardian(Base):
    __tablename__ = "guardian"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    price = Column(Integer)
    status = Column(String)
# ______________________________________________________________________
class HasakiLink(Base):
    __tablename__ = "hasaki_link"

    id = Column(Integer, primary_key=True, autoincrement=True)
    link = Column(String)



class Hasaki(Base):
    __tablename__ = 'hasaki'

    id = Column(Integer, primary_key=True)
    name = Column(String(500))
    price = Column(Integer)
    total = Column(Integer)
    status = Column(String(45))


    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    price = Column(Integer)
    total = Column(Integer)
    status = Column(String)

# pharmacity________________________________________________________________
class Pharmacity(Base):
    __tablename__ = "pharmacity"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    price = Column(Integer)
    total = Column(Integer)
    brick_price = Column(Integer)

class PharmacityLink(Base):
    __tablename__ = "pharmacity_link"
    id = Column(Integer, primary_key=True, autoincrement=True)
    link = Column(String)

# watson____________________________________________________________________
class WatsonLink(Base):
    __tablename__ = "watson_link"

    id = Column(Integer, primary_key=True, autoincrement=True)
    link = Column(String)

class Watson(Base):
    __tablename__ = "watson"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    price = Column(Integer)
    total = Column(Integer)
