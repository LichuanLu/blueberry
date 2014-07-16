# coding: utf-8
__author__ = 'bertramlau(moodspace@gmail.com)'

import config

import sqlalchemy as sa
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy import exc

class LookLively(object):
    """Ensures that MySQL connections checked out of the pool are alive."""
    def checkout(self, dbapi_con, con_record, con_proxy):
        try:
            try:
                dbapi_con.ping(False)
            except TypeError:
                dbapi_con.ping()
        except dbapi_con.OperationalError, ex:
            if ex.args[0] in (2006, 2013, 2014, 2045, 2055):
                raise exc.DisconnectionError()
            else:
                raise

config = config.rec()
engine = sa.create_engine(config.database + '?charset=utf8',echo=True,pool_size=20,listeners=[LookLively()])



DB_Session = sessionmaker(bind=engine)

#db_session= DB_Session()

Base = declarative_base()
db_session=scoped_session(sessionmaker(autocommit=False,
                            autoflush=False,
                            bind=engine))


def init_db():
    import DoctorSpring.models
    Base.metadata.create_all(engine)
    print(u'数据库部署完成！')
    return
