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
    user = relationship("User", backref=backref('diagnoseLog', order_by=id))
    diagnoseId=sa.Column(sa.Integer)
    alipayNumber=sa.Column(sa.String(128))
    action=sa.Column(sa.String(128))
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
    @classmethod
    def getAlipayLogsByDiagnoseId(cls,diagnoseId):
        if diagnoseId is None:
            return
        return session.query(AlipayLog).filter(AlipayLog.diagnoseId==diagnoseId).order_by(AlipayLog.createTime).desc().all()
    @classmethod
    def getAlipayLogsByUserId(cls,userId):
        if userId is None:
            return
        return session.query(AlipayLog).filter(AlipayLog.userId==userId).order_by(AlipayLog.createTime).desc().all()

