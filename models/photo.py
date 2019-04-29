from sqlalchemy import Table, Column, Integer, String
from models.base import Base, metadata
from config.database import *


class Photo(Base):
    __tablename__ = photos
    id = Column(Integer, autoincrement=True, primary_key=True)
    file_id = Column(String, index=True)
    access_hash = Column(String, index=True)
    name = Column(String, index=True)
    file_size = Column(Integer, index=True)
    mime_type = Column(String, index=True)
    width = Column(Integer, index=True)
    height = Column(Integer, index=True)
    ext_width = Column(Integer, index=True)
    ext_height = Column(Integer, index=True)

    def __init__(self, file_id, access_hash, name, file_size, mime_type, width, height, ext_width, ext_height):
        self.file_id = file_id
        self.access_hash = access_hash
        self.name = name
        self.file_size = file_size
        self.mime_type = mime_type
        self.width = width
        self.height = height
        self.ext_width = ext_width
        self.ext_height = ext_height

    def __repr__(self):
        return '{id: "%s", file_id: "%s",access_hash: "%s",name: "%s",file_size: "%s",mime_type: "%s", ' \
               'width: "%s", height: "%s", ext_width: "%s", ext_height: "%s"}' % (
                   self.id, self.file_id, self.access_hash, self.name, self.file_size, self.mime_type,
                   self.width, self.height, self.ext_width, self.ext_height)


photos = Table(photos, metadata,
               Column('id', Integer, primary_key=True, autoincrement=True),
               Column('file_id', Integer),
               Column('access_hash', String),
               Column('name', String),
               Column('file_size', Integer),
               Column('mime_type', String),
               Column('width', Integer),
               Column('height', Integer),
               Column('ext_width', Integer),
               Column('ext_height', Integer)
               )
