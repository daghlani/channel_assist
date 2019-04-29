from sqlalchemy import Table, Column, Integer, String
from models.base import Base, metadata
from config.database import *


class User(Base):
    __tablename__ = users
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, unique=True)
    user_accessHash = Column(String)
    name = Column(String)
    username = Column(String, default=None)

    def __init__(self, user_id, user_accessHash, name, username):
        self.user_id = user_id
        self.user_accessHash = user_accessHash
        self.name = name
        self.username = username

    def __repr__(self):
        return "<User(user_id='%s', user_accessHash='%s', name='%s', username='%s')>" % (
            self.user_id, self.user_accessHash, self.name, self.username)


users = Table(users, metadata,
              Column('id', Integer, primary_key=True, autoincrement=True),
              Column('user_id', Integer, unique=True),
              Column('user_accessHash'),
              Column('name'),
              Column('username')
              )
