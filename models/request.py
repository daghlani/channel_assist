from sqlalchemy import Table, Column, Integer, String, Text, DateTime
from models.base import Base, metadata
from config.database import *
import datetime


class Request(Base):
    __tablename__ = requests
    id = Column(Integer, primary_key=True, autoincrement=True)
    date = Column(DateTime, default=datetime.datetime.now().__format__("%Y-%m-%d %H:%M:%S.%f"))
    user_id = Column(Integer)
    request_id = Column(String)
    count = Column(String)
    amount = Column(String)
    state = Column(String, default=default_state)
    description = Column(Text)

    def __init__(self, user_id, request_id, count, amount, state, description):
        self.user_id = user_id
        self.request_id = request_id
        self.count = count
        self.amount = amount
        self.state = state
        self.description = description

    def __repr__(self):
        return "<User(date= '%s', user_id='%s', request_id= '%s', count='%s', amount='%s', , state= '%s', " \
               "description='%s')>" % (
                   self.date, self.user_id, self.request_id, self.count, self.amount, self.state, self.description)


requests = Table(requests, metadata,
                 Column('id', Integer, primary_key=True, autoincrement=True),
                 Column('date', DateTime),
                 Column('user_id', Integer),
                 Column('request_id', String),
                 Column('count', String),
                 Column('amount', String),
                 Column('state', String),
                 Column('description', Text)
                 )
