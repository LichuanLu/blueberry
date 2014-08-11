__author__ = 'chengc017'

import sqlalchemy as sa
from sqlalchemy.orm import relationship,backref

from database import Base,db_session as session
from DoctorSpring.util.constant import ModelStatus
import time
from DoctorSpring.models import File

from flask.ext.sqlalchemy import SQLAlchemy
from DoctorSpring import app
from datetime import datetime
class AlipayLog(Base):
    __tablename__ = 'alipayLog'
    __table_args__ = {
        'mysql_charset': 'utf8',
        'mysql_engine': 'MyISAM',

    }

    id = sa.Column(sa.Integer, primary_key = True, autoincrement = True)
    userId = sa.Column(sa.Integer,sa.ForeignKey('user.id'))
    user = relationship("User", backref=backref('alipayLog', order_by=id))
    diagnoseId=sa.Column(sa.Integer)
    alipayNumber=sa.Column(sa.String(128))
    action=sa.Column(sa.String(128))
    payUrl=sa.Column(sa.String(1024))
    description=sa.Column(sa.String(624))
    createTime=sa.Column(sa.DateTime)
    def __init__(self,userId,diagnoseId,action):
        self.userId=userId
        self.diagnoseId=diagnoseId
        self.action=action
        self.createTime=datetime.now()
    @classmethod
    def save(cls,alipayLog):
        if alipayLog is None:
            return
        session.add(alipayLog)
        session.commit()
        session.flush()
    @classmethod
    def getAlipayLogsByDiagnoseId(cls,diagnoseId):
        if diagnoseId is None:
            return
        return session.query(AlipayLog).filter(AlipayLog.diagnoseId==diagnoseId).order_by(AlipayLog.createTime.desc()).all()
    @classmethod
    def getAlipayLogsByUserId(cls,userId):
        if userId is None:
            return
        return session.query(AlipayLog).filter(AlipayLog.userId==userId).order_by(AlipayLog.createTime.desc()).all()


class AlipayChargeRecord(Base):
    __tablename__ = 'alipayChargeRecord'
    __table_args__ = {
        'mysql_charset': 'utf8',
        'mysql_engine': 'MyISAM',

        }

    id = sa.Column(sa.Integer, primary_key = True, autoincrement = True)
    userId = sa.Column(sa.Integer,sa.ForeignKey('user.id'))
    user = relationship("User", backref=backref('alipayChargeRecord', order_by=id))
    diagnoseSeriesNumber = sa.Column(sa.String(256))
    alipayNumber=sa.Column(sa.String(128))
    buyer_email=sa.Column(sa.String(128))
    buyer_id=sa.Column(sa.String(256))
    is_success=sa.Column(sa.Integer)
    notify_time=sa.Column(sa.DateTime)
    notify_type=sa.Column(sa.Integer)
    total_fee=sa.Column(sa.Float)
    trade_no =sa.Column(sa.String(256))
    out_trade_no =sa.Column(sa.String(256))
    trade_status= sa.Column(sa.String(256))
    description=sa.Column(sa.String(624))
    createTime=sa.Column(sa.DateTime)

    def __init__(self,diagnoseSeriesNumber,buyer_email,buyer_id,is_success,notify_time,notify_type,total_fee,trade_no,trade_status,
                 out_trade_no):
        self.diagnoseSeriesNumber=diagnoseSeriesNumber
        self.buyer_email=buyer_email
        self.buyer_id=buyer_id
        self.is_success=is_success
        self.notify_time=notify_time
        self.notify_type=notify_type
        self.total_fee=total_fee
        self.trade_no=trade_no
        self.trade_status=trade_status
        self.out_trade_no=out_trade_no
    @classmethod
    def save(cls,record):
        if record is None:
            return
        session.add(record)
        session.commit()
        session.flush()