# coding: utf-8
__author__ = 'bertramlau(moodspace@gmail.com)'

import config

import sqlalchemy as sa
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker

config = config.rec()
engine = sa.create_engine(config.database + '?charset=utf8')

DB_Session = sessionmaker(bind=engine)
db_session = DB_Session()

Base = declarative_base()


def init_db():
    import DoctorSpring.models
    Base.metadata.create_all(engine)
    print(u'数据库部署完成！')
    return
