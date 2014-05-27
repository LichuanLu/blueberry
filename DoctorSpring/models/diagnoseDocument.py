# coding: utf-8
__author__ = 'chengc017'

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
from DoctorSpring.util.constant import Pagger,SystemTimeLimiter,DiagnoseStatus,ReportStatus,ReportType,\
    SeriesNumberPrefix,SeriesNumberBase
from datetime import datetime
from database import Base,db_session as session
from sqlalchemy.orm import relationship,backref

import uuid

class Diagnose(Base):
    __tablename__ = 'diagnose'
    __table_args__ = {
        'mysql_charset': 'utf8',
        }

    id = sa.Column(sa.Integer, primary_key = True, autoincrement = True)
    patientId  = sa.Column(sa.Integer,sa.ForeignKey('patent.id'))
    patient = relationship("Patent", backref=backref('diagnose', order_by=id))

    doctorId  = sa.Column(sa.Integer,sa.ForeignKey('doctor.id'))
    doctor = relationship("Doctor", backref=backref('diagnose', order_by=id))

    adminId = sa.Column(sa.INTEGER)

    uploadUserId  = sa.Column(sa.Integer,sa.ForeignKey('User.id'))
    uploadUser = relationship("User", backref=backref('diagnose', order_by=id))

    pathologyId=sa.Column(sa.Integer,sa.ForeignKey('pathology.id'))
    pathology=relationship("Pathology", backref=backref('diagnose', order_by=id))

    reportId = sa.Column(sa.Integer,sa.ForeignKey('report.id'))
    report=relationship("Report", backref=backref('diagnose', order_by=id))

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

    @classmethod
    def getDiagnoseById(cls,diagnoseId):
        if diagnoseId:
            return session.query(Diagnose).filter(Diagnose.id==diagnoseId,Diagnose.status==DiagnoseStatus.Diagnosed).first()


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




class Report(Base):
    __tablename__ = 'report'
    __table_args__ = {
        'mysql_charset': 'utf8',
        }

    id = sa.Column(sa.Integer, primary_key = True, autoincrement = True)
    seriesNumber=sa.Column(sa.String(256))
    fileUrl=sa.Column(sa.String(256))
    techDesc=sa.Column(sa.String(512))
    imageDesc=sa.Column(sa.TEXT)
    diagnoseDesc=sa.Column(sa.String(512))
    type=sa.Column(sa.Integer)
    status=sa.Column(sa.Integer)
    createDate= sa.Column(sa.DateTime)
    #sa.Index('diagnoseTemplate_method_position_diagnoseDesc', 'diagnoseMethod', 'diagnosePosition','diagnoseDesc')

    def __init__(self,techDesc=None,imageDesc=None,diagnoseDesc=None,fileUrl=None,type=ReportType.Doctor,status=ReportStatus.Draft):
        maxId=Report.getMaxId()
        if maxId:
            maxId=1
        self.seriesNumber='%s%i'%(SeriesNumberPrefix,SeriesNumberBase+maxId)
        self.fileUrl=fileUrl
        self.techDesc=techDesc
        self.imageDesc=imageDesc
        self.diagnoseDesc=diagnoseDesc
        self.type=type
        self.createDate=datetime.now()
        if status:
            self.status=status
        else:
            self.status=ReportStatus.Draft
    @classmethod
    def getMaxId(cls):
        from sqlalchemy.sql import func
        return session.query(func.max(Report.id)).first()
    @classmethod
    def save(cls,report):
        if report:
            session.add(report)
            session.commit()
            session.flush()
    @classmethod
    def getReportById(cls,reportId):
        if reportId:
            return session.query(Report).filter(Report.id==reportId).first()
    @classmethod
    def update(cls,reportId,type=None,status=None,fileUrl=None,techDesc=None,imageDesc=None,diagnoseDesc=None):
        if reportId is None:
            return
        report=session.query(Report).filter(Report.id==reportId).first()
        if report:
            if type:
                report.type=type
            if status:
                report.status=status
            if fileUrl:
                report.fileUrl=fileUrl
            if techDesc:
                report.techDesc=techDesc
            if imageDesc:
                report.imageDesc=imageDesc
            if diagnoseDesc:
                report.diagnoseDesc=diagnoseDesc
        session.commit()
        session.flush()
        return report

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