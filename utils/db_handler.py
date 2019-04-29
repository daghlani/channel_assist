from models.request import Request
from models.photo import Photo
from models.user import User
from models.product import *
from models.base import *

Base.metadata.create_all(engine)
session = Session()


def creat_table_if_not_exist(db_engine, table):
    if db_engine.has_table(table) is not True:
        table.create(bind=db_engine)
        logger.info('%s created.' % table)
    else:
        logger.debug('%s exist.' % table)


def add_user_if_not_exist(update):
    try:
        profile = update.users[0]
        user_id = profile.id
        name = profile.name
        username = profile.username
        user_accessHash = profile.access_hash
        user = session.query(User).filter(User.user_id == user_id).one_or_none()
        if not user:
            user = User(user_id=user_id, user_accessHash=user_accessHash, name=name, username=username)
            session.add(user)
        session.commit()
    except Exception as err:
        session.rollback()
        logger.error("add_user_if_not_exist error [%s]", err)


def select_prd(prd_id):
    try:
        res = session.query(Product).filter(Product.id == prd_id).first()
        return res
    except Exception as err:
        logger.error("select_prd error [%s]", err)


def select_photo_file_id(file_id):
    try:
        res = session.query(Photo.id).filter(Photo.file_id == file_id).first()
        return res
    except Exception as err:
        logger.error("select_photo_file_id error [%s]", err)


def select_photo_id(photo_id):
    try:
        res = session.query(Photo).filter(Photo.id == photo_id).first()
        return res
    except Exception as err:
        logger.error("select_photo_id error [%s]", err)


def select_state(req_id):
    try:
        res = session.query(Request.state).filter(Request.request_id == req_id).first()[0]
        return res
    except Exception as err:
        logger.error("select_state error [%s]", err)


def insert_photo(file_id, access_hash, name, file_size, mime_type, width, height, ext_width, ext_height):
    try:
        pto = Photo(file_id=file_id, access_hash=access_hash, name=name, file_size=file_size, mime_type=mime_type,
                    width=width, height=height, ext_width=ext_width, ext_height=ext_height)
        session.add(pto)
        session.commit()
    except Exception as err:
        logger.error("insert_photo error [%s]", err)


def insert_product(name, amount, photo_id):
    try:
        prd = Product(name=name, amount=amount, photo_id=photo_id)
        session.add(prd)
        session.commit()
    except Exception as err:
        logger.error("insert_product error [%s]", err)


def insert_request(user_id, request_id, count, amount, description):
    try:
        req = Request(user_id=user_id, request_id=request_id, count=count, amount=amount, description=description,
                      state=None)
        session.add(req)
        session.commit()
    except Exception as err:
        logger.error("insert_request error [%s]", err)
