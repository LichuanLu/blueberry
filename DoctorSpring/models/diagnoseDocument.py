# coding: utf-8
__author__ = 'Jeremy'

import sqlalchemy as sa
from  sqlalchemy import distinct

from database import Base
from sqlalchemy.orm import  relationship,backref


# class Post(Base):
#     __tablename__ = 'diagnose'
#     __table_args__ = {
#         'mysql_charset': 'utf8',
#         }
#
#     id = sa.Column(sa.Integer, primary_key = True, autoincrement = True)
#     userId  = sa.Column(sa.Integer)
#     pathologyId = sa.Column(sa.INTEGER)  #病理信息表ID
#     patientId = sa.Column(sa.INTEGER)    #病人表ID
#     createDate = sa.Column(sa.DATETIME)
#     reviewDate = sa.Column(sa.DATETIME)
#     adminId = sa.Column(sa.INTEGER)     #审查adminID
#     reportId = sa.Column(sa.INTEGER)    #生成reportID
#     hospitalId = sa.Column(sa.INTEGER)  #医院ID，用于医院批量提交诊断信息
#     status = sa.Column(sa.INTEGER)      #标记状态 未提交，待审查，待诊断，待审核，结束
# coding: utf-8
__author__ = 'chengc017'

import sqlalchemy as sa
from DoctorSpring.util.constant import Pagger,SystemTimeLimiter,DiagnoseStatus
from datetime import datetime
from database import Base,db_session as session
from sqlalchemy.orm import relationship,backref

class Diagnose(Base):
    __tablename__ = 'diagnose'
    __table_args__ = {
        'mysql_charset': 'utf8',
        }

    id = sa.Column(sa.Integer, primary_key = True, autoincrement = True)
    patientId  = sa.Column(sa.Integer,sa.ForeignKey('patient.id'))
    patient = relationship("Patient", backref=backref('diagnose', order_by=id))

    doctorId  = sa.Column(sa.Integer,sa.ForeignKey('doctor.id'))
    doctor = relationship("Doctor", backref=backref('diagnose', order_by=id))

    adminId = sa.Column(sa.INTEGER)

    uploadUserId  = sa.Column(sa.Integer,sa.ForeignKey('User.id'))
    uploadUser = relationship("User", backref=backref('diagnose', order_by=id))

    pathologyId  = sa.Column(sa.Integer,sa.ForeignKey('pathology.id'))
    pathology = relationship("Pathology", backref=backref('diagnose', order_by=id))

    reportId = sa.Column(sa.Integer)
    score = sa.Column(sa.Integer)

    createDate=sa.Column(sa.DateTime)
    reviewDate = sa.Column(sa.DATETIME)

    hospitalId = sa.Column(sa.INTEGER)  #医院ID，用于医院批量提交诊断信息
    status = sa.Column(sa.INTEGER)

    @classmethod
    def save(cls,diagnose):
        if diagnose:
            session.add(diagnose)
            session.commit()
            session.flush()
    @classmethod
    def getDiagnosesByDoctorId(cls,doctorId,pagger,status=None,startTime=SystemTimeLimiter.startTime,endTime=SystemTimeLimiter.endTime):
        count=Diagnose.getDiagnoseCountByDoctorId(doctorId,status,startTime,endTime)
        pagger.count=count
        if doctorId:
            if status:
                return session.query(Diagnose).filter(Diagnose.doctorId==doctorId,Diagnose.status==status,
                                                      Diagnose.createDate>startTime,Diagnose.createDate<endTime)\
                    .offset(pagger.getOffset()).limit(pagger.getLimitCount()).all()
            else:
                return session.query(Diagnose).filter(Diagnose.doctorId==doctorId,Diagnose.status!=DiagnoseStatus.Del,
                                                      Diagnose.createDate>startTime,Diagnose.createDate<endTime) \
                    .offset(pagger.getOffset()).limit(pagger.getLimitCount()).all()
    @classmethod
    def getDiagnoseCountByDoctorId(cls,doctorId,status=None,startTime=SystemTimeLimiter.startTime,endTime=SystemTimeLimiter.endTime):
        if doctorId:
            if status:
                return session.query(Diagnose).filter(Diagnose.doctorId==doctorId,Diagnose.status==status,
                                                      Diagnose.createDate>startTime,Diagnose.createDate<endTime).count()
            else:
                return session.query(Diagnose).filter(Diagnose.doctorId==doctorId,Diagnose.status!=DiagnoseStatus.Del,
                                                      Diagnose.createDate>startTime,Diagnose.createDate<endTime).count()
    @classmethod
    def getNewDiagnoseCountByDoctorId(cls,doctorId):
        if doctorId:
            return session.query(Diagnose).filter(Diagnose.doctorId==doctorId,Diagnose.status==DiagnoseStatus.NeedDiagnose).count()
    @classmethod
    def getPatientListByDoctorId(cls,doctorId):
        if doctorId:
            diagnoses =session.query(Diagnose).filter(Diagnose.doctorId==doctorId,Diagnose.status==DiagnoseStatus.Diagnosed).group_by(Diagnose.patientId).all()
            if diagnoses and len(diagnoses)>0:
                patients=[]
                for diagnose in diagnoses:
                    patients.append(diagnose.patient)
                return patients


class DiagnoseTemplate(Base):
    __tablename__ = 'diagnoseTemplate'
    __table_args__ = {
        'mysql_charset': 'utf8',
        }

    id = sa.Column(sa.Integer, primary_key = True, autoincrement = True)
    diagnoseMethod=sa.Column(sa.String(256))
    diagnosePosition=sa.Column(sa.String(256))
    techDesc=sa.Column(sa.String(512))
    imageDesc=sa.Column(sa.TEXT)
    diagnoseDesc=sa.Column(sa.String(512))
    #sa.Index('diagnoseTemplate_method_position_diagnoseDesc', 'diagnoseMethod', 'diagnosePosition','diagnoseDesc')

    def __init__(self,diagnoseMethod,diagnosePosition,techDesc,imageDesc,diagnoseDesc):
        self.diagnoseMethod=diagnoseMethod
        self.diagnosePosition=diagnosePosition
        self.techDesc=techDesc
        self.imageDesc=imageDesc
        self.diagnoseDesc=diagnoseDesc

    @classmethod
    def save(cls,diagnoseTemplate):
        if diagnoseTemplate:
            session.add(diagnoseTemplate)
            session.commit()
            session.flush()
    @classmethod
    def getDiagnosePostion(cls,diagnoseMethod):
        if diagnoseMethod:
            return session.query(DiagnoseTemplate.diagnosePosition).filter(DiagnoseTemplate.diagnoseMethod==diagnoseMethod)\
                .group_by(DiagnoseTemplate.diagnosePosition).all()
    @classmethod
    def getDiagnoseAndImageDescs(cls,diagnoseMethod,diagnosePosition):
        if diagnoseMethod and diagnosePosition:
            return session.query(DiagnoseTemplate.diagnosePosition,DiagnoseTemplate.diagnoseDesc,
                                 DiagnoseTemplate.imageDesc).filter(DiagnoseTemplate.diagnoseMethod==diagnoseMethod,
                                                                           DiagnoseTemplate.diagnosePosition==diagnosePosition) \
                .group_by(DiagnoseTemplate.diagnoseDesc).all()



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