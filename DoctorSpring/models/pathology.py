# coding: utf-8
__author__ = 'chengc017'

import sqlalchemy as sa
from sqlalchemy.orm import relationship,backref

from database import Base,db_session as session
from DoctorSpring.util.constant import ModelStatus


class Pathology(Base):
    __tablename__ = 'pathology'
    __table_args__ = {
        'mysql_charset': 'utf8',
        'mysql_engine': 'MyISAM',
    }

    id = sa.Column(sa.Integer, primary_key = True, autoincrement = True)
    hospticalId = sa.Column(sa.INTEGER)    #医院ID
    #diagnoseDocId = sa.Column(sa.INTEGER)  #诊断表ID
    #diagnosePartId = sa.Column(sa.INTEGER)  #检查部位ID
    caseHistory = sa.Column(sa.TEXT)       #病史
    diagnoseMethod=sa.Column(sa.String(32))
    #  docmFileId=sa.Column(sa.INTEGER)
    status = sa.Column(sa.INTEGER)      #标记状态 未提交，待审查，待诊断，待审核，结束
    pathologyPostions= relationship("PathologyPostion", order_by="PathologyPostion.id", backref="Pathology")
    pathologyFiles=relationship("File2Pathology", order_by="File2Pathology.id", backref="Pathology")

    def __init__(self):
        self.status = ModelStatus.Normal


    @classmethod
    def save(cls, pathology):
        if pathology:
            session.add(pathology)
            session.commit()
            session.flush()
    @classmethod
    def getById(cls,id):
        if id:
            return session.query(Pathology).filter(Pathology.id == id,Pathology.status == ModelStatus.Normal).first()
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



class File2Pathology(Base):
    __tablename__ = 'file2pathology'
    __table_args__ = {
        'mysql_charset': 'utf8',
        'mysql_engine': 'MyISAM',
    }

    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)


    pathologyId = sa.Column(sa.INTEGER, sa.ForeignKey('pathology.id'))
    pathology = relationship("Pathology", backref=backref('File2Pathology', order_by=id))
    fileurl = sa.Column(sa.String(255))

    status = sa.Column(sa.INTEGER)

    def __init__(self, pathologyId=pathologyId, fileurl=fileurl):
        self.pathologyId = pathologyId
        self.fileurl = fileurl
        self.status = ModelStatus.Normal

    @classmethod
    def save(cls, file2pathology):
        if file2pathology:
            session.add(file2pathology)
            session.commit()
            session.flush()


