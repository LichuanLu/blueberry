# coding: utf-8
__author__ = 'chengc017'

import sqlalchemy as sa
from sqlalchemy.orm import  relationship,backref,join

from database import Base ,db_session as session
from DoctorSpring.util.constant import ModelStatus, UserStatus



class Patient(Base):
    __tablename__ = 'patient'
    __table_args__ = {
        'mysql_charset': 'utf8',
    }

    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    userID = sa.Column(sa.Integer,sa.ForeignKey('user.id'))
    user = relationship("User", backref=backref('patient', order_by=id))

    locationId = sa.Column(sa.INTEGER)     #所在地ID
    identityCode = sa.Column(sa.String(64))
    gender = sa.Column(sa.INTEGER)
    birthDate = sa.Column(sa.DateTime)
    realname = sa.Column(sa.String(64))
    yibaoCode = sa.Column(sa.INTEGER)
    identityPhone = sa.Column(sa.INTEGER)

    type = sa.Column(sa.INTEGER)   # 0:历史记录, 1:注册用户
    status = sa.Column(sa.INTEGER)

    def __init__(self, userId=None):
        self.userID = userId
        self.status = ModelStatus.Normal

    @classmethod
    def save(cls, patient):
        if patient:
            session.add(patient)
            session.commit()
            session.flush()

'''
    def __repr__(self):
        return '<Post %s>' % (self.title)
'''