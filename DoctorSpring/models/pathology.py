# coding: utf-8
__author__ = 'chengc017'

import sqlalchemy as sa
from sqlalchemy.orm import relationship,backref

from database import Base,db_session as session
from DoctorSpring.util.constant import ModelStatus
from datetime import time


class Pathology(Base):
    __tablename__ = 'pathology'
    __table_args__ = {
        'mysql_charset': 'utf8',
        'mysql_engine': 'MyISAM',
    }

    id = sa.Column(sa.Integer, primary_key = True, autoincrement = True)
    patientId = sa.Column(sa.INTEGER, sa.ForeignKey('patient.id'))
    patient = relationship("Patient", backref=backref('pathology', order_by=id))
    hospticalId = sa.Column(sa.INTEGER)    #医院ID
    #diagnoseDocId = sa.Column(sa.INTEGER)  #诊断表ID
    #diagnosePartId = sa.Column(sa.INTEGER)  #检查部位ID
    name = sa.Column(sa.String(32))
    caseHistory = sa.Column(sa.TEXT)       #病史
    diagnoseMethod=sa.Column(sa.String(32))
    #  docmFileId=sa.Column(sa.INTEGER)
    status = sa.Column(sa.INTEGER)      #标记状态 未提交，待审查，待诊断，待审核，结束
    pathologyPostions = relationship("PathologyPostion", order_by="PathologyPostion.id", backref="Pathology")

    def __init__(self):
        self.status = ModelStatus.Normal

    @classmethod
    def set_name(id):
        Pathology.name = id + '-' + time.strftime('%Y-%m-%d', time.localtime(time.time()))

    @classmethod
    def save(cls, pathology):
        if pathology:
            session.add(pathology)
            session.commit()
            session.flush()
    @classmethod
    def getById(cls,id):
        if id:
            return session.query(Pathology).filter(Pathology.id == id).first()

    @classmethod
    def getByPatientId(cls,id):
        if id:
            return session.query(Pathology).filter(Pathology.patientId == id,Pathology.status == ModelStatus.Normal).all()

class Position(Base):

    __tablename__ = 'position'
    __table_args__ = {
        'mysql_charset': 'utf8',
        'mysql_engine': 'MyISAM',
    }

    id = sa.Column(sa.Integer, primary_key = True, autoincrement = True)
    name=sa.Column(sa.String(512))
    parentId=sa.Column(sa.Integer)
    status=sa.Column(sa.Integer)


    @classmethod
    def save(cls,position):
        if position:
            session.add(position)
            session.commit()
            session.flush()

class PathologyPostion(Base):
    __tablename__ = 'pathologyPostion'
    __table_args__ = {
        'mysql_charset': 'utf8',
        'mysql_engine': 'MyISAM',
    }

    id = sa.Column(sa.Integer, primary_key = True, autoincrement = True)
    pathologyId=sa.Column(sa.Integer,sa.ForeignKey('pathology.id'))
    pathology=relationship("Pathology", backref=backref('pathologyPostion', order_by=id))
    positionId=sa.Column(sa.Integer,sa.ForeignKey('position.id'))
    position=relationship("Position", backref=backref('pathologyPostion', order_by=id))



    def __init__(self, pathologyId=pathologyId, positionId=positionId):
        self.pathologyId = pathologyId
        self.positionId = positionId
        self.status = ModelStatus.Normal

    @classmethod
    def save(cls,pathologyPostion):
        if pathologyPostion:
            session.add(pathologyPostion)
            session.commit()
            session.flush()




