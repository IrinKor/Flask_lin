# -*- coding: UTF-8 -*-
from sqlalchemy import Column,  Integer,Float,Date,  DateTime, Text, Boolean,BigInteger, String, ForeignKey, or_, not_
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import relationship, query_expression
from sqlalchemy.sql import func
from database import Base, db_session, engine as db_engine
from sqlalchemy.ext.declarative import declarative_base
import datetime

class Root:
    @classmethod
    def load_limited(cls, page=1, cnt=10):
        return (db_session.query(cls).offset((page-1)*cnt).limit(cnt).all(), db_session.query(cls).count()//cnt)

class Set(Base,Root):
    __tablename__ = 'sets'
    id    = Column(Integer, primary_key=True)
    set_num = Column(String(20))
    name = Column(String(256))
    year = Column(Integer)
    theme_id = Column(Integer)
    num_parts = Column(Integer)
    @classmethod
    def search_by_name(cls, query):
        return db_session.query(cls).filter(Set.name.like("%"+query+"%")).all()

class Subscriber(Base):
    __tablename__='subscribers'
    id = Column(Integer, primary_key=True)
    tg_id = Column(BigInteger)
    login = Column(String(50))
    fio = Column(String(100))
    flat = Column(String(100))
    #message = Column(String(500))
    status = Column(Boolean)

class Message(Base):
    __tablename__='messages'
    id = Column(Integer, primary_key=True)
    msg = Column(String(500))
    is_incomming = Column(Boolean)
    created = Column(DateTime)
    subscr_id = Column(Integer)


Base = declarative_base()

class Favorite(Base):
    __tablename__ = 'favorites'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer)  # или session_id для простоты
    set_num = Column(String, ForeignKey('sets.set_num'))
    # Добавить связь если нужно
    # set = relationship("Set")

class Parts(Base,Root):
    __tablename__ = 'parts'
    id    = Column(Integer, primary_key=True)
    part_num = Column(String(20))
    name = Column(String(256))
    part_cat_id = Column(Integer)



def init_db():
    # import all modules here that might define models so that
    # they will be registered properly on the metadata.  Otherwise
    # you will have to import them first before calling init_db()
    from database import engine
    Base.metadata.create_all(bind=engine)
    db_session.commit()

def print_schema(table_class):
    from sqlalchemy.schema import CreateTable, CreateColumn
    print(str(CreateTable(table_class.__table__).compile(db_engine)))

def print_columns(table_class, *attrNames):
   from sqlalchemy.schema import CreateTable, CreateColumn
   c = table_class.__table__.c
   print( ',\r\n'.join((str( CreateColumn(getattr(c, attrName)).compile(db_engine)) \
                            for attrName in attrNames if hasattr(c, attrName)
               )))

if __name__ == "__main__":
    init_db()
    example_1()
    example_3()
    #print_columns(Payment, "created")
    #print_schema(SoltButton)
