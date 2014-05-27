# coding: utf-8
__author__ = 'Jeremy'
# coding: utf-8

import sqlalchemy as sa

from database import Base,db_session as session
from DoctorSpring.util.constant import ModelStatus, UserStatus
from sqlalchemy.orm import relationship, backref
import config


class Doctor(Base):
    __tablename__ = 'doctor'
    __table_args__ = {
        'mysql_charset': 'utf8',
        }

    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    userId = sa.Column(sa.Integer, sa.ForeignKey('User.id'))     #对应User表里的ID
    user = relationship("User", backref=backref('doctor', order_by=id))
    username = sa.Column(sa.String(64))
    identityPhone = sa.Column(sa.INTEGER)
    title = sa.Column(sa.String(64))    #职称
    hospitalId = sa.Column(sa.INTEGER)  #医院ID
    departmentId = sa.Column(sa.INTEGER)  #科室ID
    skillId = sa.Column(sa.INTEGER)       #擅长
    description = sa.Column(sa.TEXT)
    diagnoseCount = sa.Column(sa.INTEGER)   #统计，诊断量
    feedbackCount = sa.Column(sa.INTEGER)   #好评数
    auditCount = sa.Column(sa.INTEGER)      #审核量
    type = sa.Column(sa.INTEGER)
    status = sa.Column(sa.INTEGER)

    def __init__(self, userId=None):
        self.userId = userId
        self.title = config.DEFAULT_TITLE
        self.status = ModelStatus.Normal

    @classmethod
    def getById(cls,doctorId):
        if doctorId is None or doctorId<1:
            return
        return session.query(Doctor).filter(Doctor.id==doctorId,Doctor.status==ModelStatus.Normal).first()

    @classmethod
    def save(cls, doctor):
        if doctor:
            session.add(doctor)
            session.commit()
            session.flush()


'''
    def __init__(self, title=title, content=content, origin_content=None,
                 created_date=None, update_date=None):
        self.title = title
        self.content = content
        self.update_date = update_date
        if created_date == None:
            self.created_date = time.time()
        else:
            self.created_date = created_date
        if origin_content == None:
            self.origin_content = content
        else:
            self.origin_content = origin_content


    def __repr__(self):
        return '<Post %s>' % (self.title)
'''