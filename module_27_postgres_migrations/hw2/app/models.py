from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, ARRAY, JSON
from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy.ext.mutable import MutableList

Base = declarative_base()


class Coffee(Base):
    __tablename__ = 'coffee'

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), nullable=False)
    category = Column(String(200))
    description = Column(String(200))
    reviews = Column(MutableList.as_mutable(ARRAY(String)))


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), nullable=False)
    has_sale = Column(Boolean)
    address = Column(JSON)
    coffee_id = Column(Integer, ForeignKey('coffee.id'))

    coffee = relationship("Coffee")