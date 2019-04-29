from sqlalchemy import Table, Column, Integer, String
from models.base import Base, metadata
from config.database import *


class Product(Base):
    __tablename__ = products
    id = Column(Integer, autoincrement=True, primary_key=True)
    name = Column(String, index=True)
    amount = Column(Integer, index=True)
    photo_id = Column(Integer, index=True)

    def __init__(self, name, amount, photo_id):
        self.name = name
        self.amount = amount
        self.photo_id = photo_id

    def __repr__(self):
        return '{id: "%s", name: "%s", amount: "%s", photo_id: "%s"}' % (
            self.id, self.name, self.amount, self.photo_id)


products = Table(products, metadata,
                 Column('id', Integer, primary_key=True, autoincrement=True),
                 Column('name', String),
                 Column('amount', Integer),
                 Column('photo_id', Integer)
                 )
