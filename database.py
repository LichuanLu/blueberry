# coding: utf-8
__author__ = 'bertramlau(moodspace@gmail.com)'

import config

import sqlalchemy as sa
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy import exc
from sqlalchemy.pool import Pool,event

@event.listens_for(Pool, "checkout")
def ping_connection(dbapi_connection, connection_record, connection_proxy):
    cursor = dbapi_connection.cursor()
    try:
        cursor.execute("SELECT 1")
    except:
        # optional - dispose the whole pool
        # instead of invalidating one at a time
        # connection_proxy._pool.dispose()

        # raise DisconnectionError - pool will try
        # connecting again up to three times before raising.
        raise exc.DisconnectionError()
    cursor.close()

config = config.rec()
engine = sa.create_engine(config.database + '?charset=utf8',echo=True,pool_size=5,pool_recycle=60)



#DB_Session = sessionmaker(bind=engine)

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
