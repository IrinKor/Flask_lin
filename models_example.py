# -*- coding: UTF-8 -*-
from sqlalchemy import Column,  Integer,Float,Date,  DateTime, Text, Boolean, String, ForeignKey, or_, not_
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import relationship, query_expression
from sqlalchemy.sql import func
from database import Base, db_session, engine as db_engine
import datetime


class Student(Base):
    __tablename__ = 'students'
    id    = Column(Integer, primary_key=True)
    fio = Column(String(100), nullable=False, default="")
    birthday = Column(Date, nullable=False)
    sex = Column(Boolean, default=False) # M - true Ж - false
    group_id = Column(Integer, ForeignKey('groups.id'), doc="Группа студента")
    note = Column(Text, doc="Пометки")

    group = relationship("Group", back_populates="students")


class Group(Base):
    __tablename__ = 'groups'
    id    = Column(Integer, primary_key=True)
    label = Column(String(20), unique=True)
    year = Column(Integer)
    kafedra_id = Column(Integer)
    facultet_id  = Column(Integer)

    students =  relationship("Student", back_populates="group")


class Person(Base):
    __tablename__ = 'persones'
    id    = Column(Integer, primary_key=True)
    items = relationship("Inventory", back_populates="person")


class Inventory(Base):
    __tablename__ = 'inventores'
    id    = Column(Integer, primary_key=True)
    person_id = Column(Integer, ForeignKey('persones.id'))
    item_id = Column(Integer, ForeignKey('items.id'))
    person = relationship("Person", back_populates="items")
    item = relationship("Item", back_populates="persons")

class Item(Base):
    __tablename__ = 'items'
    id    = Column(Integer, primary_key=True)
    persons = relationship("Inventory", back_populates="item")




def example_1():
    """
    Добавляем группу в базу данных
    """
    g = Group(label = "ИСТ22-1", year=2022)
    db_session.add(g)
    db_session.commit()
    print(g.id) # В этот момент у нас уже есть Id
    # Добавляем студента
    s = Student(
            fio="Иванов И.И.",
            birthday = datetime.date(1987, 4, 2),
            sex = True,
            group_id = g.id

        )
    db_session.add(s)
    db_session.commit()
    print(s.id) # Теперь у нас есть id студента


def example_2():
    """
    Все тоже самое что и в 1 примере, но в одной транзакции
    """
    g = Group(label = "ИСТ22-1", year=2022)
    db_session.add(g)
    db_session.flush() # Вместо подтверждения транзакции мы вызываем данный метод
    print(g.id) # В этот момент у нас уже есть Id
    # Добавляем студента
    s = Student(
            fio="Иванов И.И.",
            birthday = datetime.date(1987, 4, 2),
            sex = True,
            group_id = g.id

        )
    db_session.add(s)
    db_session.commit()
    print(s.id) # Теперь у нас есть id студента

def example_3():
    """
    выборка данных
    """
    # Выбираем фамилии студенток и сортрируем по фио и идентификатору (последний в обратном порядке)
    query = db_session.query(Student.fio, Student.birthday)\
                .filter(Student.sex == True)\
                .order_by(Student.fio)\
                .order_by(Student.id.desc())

    for fio, in query.all():
        print(fio)

    # Выбираем всех студентов поступивших после 2022 года
    query = db_session.query(Student)\
                .join(Group)\
                .filter(Group.year >= 2022)
    for s in query.all():
        print(s.fio, s.group.year)






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
