# coding: utf-8
__author__ = 'chengc017'

import sqlalchemy as sa
from  sqlalchemy import distinct

from database import Base
from sqlalchemy.orm import  relationship,backref,join


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
    SeriesNumberPrefix,SeriesNumberBase,ModelStatus
from DoctorSpring.util import constant
from datetime import datetime
from database import Base,db_session as session
from sqlalchemy.orm import relationship,backref
import threading
from hospital import Hospital
from doctor import Doctor

import uuid
#mutex=threading.Lock()
mutex=threading.RLock()


class Diagnose(Base):
    __tablename__ = 'diagnose'
    __table_args__ = {
        'mysql_charset': 'utf8',
        }

    id = sa.Column(sa.Integer, primary_key = True, autoincrement = True)
    patientId  = sa.Column(sa.Integer,sa.ForeignKey('patient.id'))
    patient = relationship("Patient", backref=backref('diagnose', order_by=id))
    diagnoseSeriesNumber=sa.Column(sa.String(256))


    doctorId  = sa.Column(sa.Integer,sa.ForeignKey('doctor.id'))
    doctor = relationship("Doctor", backref=backref('diagnose', order_by=id))

    #adminId = sa.Column(sa.INTEGER,sa.ForeignKey('User.id'))
    #administrator = relationship("User", backref=backref('diagnose', order_by=id))
    adminId = sa.Column(sa.INTEGER)

    uploadUserId  = sa.Column(sa.Integer,sa.ForeignKey('User.id'))
    uploadUser = relationship("User", backref=backref('diagnose', order_by=id))

    pathologyId=sa.Column(sa.Integer,sa.ForeignKey('pathology.id'))
    pathology=relationship("Pathology", backref=backref('diagnose', order_by=id))

    reportId = sa.Column(sa.Integer,sa.ForeignKey('report.id'))
    report=relationship("Report", backref=backref('report', order_by=id))

    score = sa.Column(sa.Integer)

    createDate=sa.Column(sa.DateTime)
    reviewDate = sa.Column(sa.DATETIME)

    hospitalId = sa.Column(sa.Integer,sa.ForeignKey('hospital.id'))  #医院ID，用于医院批量提交诊断信息
    hospital=relationship("Hospital", backref=backref('diagnose', order_by=id))

    status = sa.Column(sa.INTEGER)

    @classmethod
    def save(cls,diagnose):
        if diagnose:
            session.add(diagnose)
            session.commit()
            if diagnose.id:
                diagnoseSeriesNumber='%s%i'%(constant.DiagnoseSeriesNumberPrefix,constant.DiagnoseSeriesNumberBase+diagnose.id)
                diagnose.diagnoseSeriesNumber=diagnoseSeriesNumber
                session.commit()
            session.flush()
    @classmethod
    def getDiagnoseById(cls,diagnoseId):
        if diagnoseId:
            return session.query(Diagnose).filter(Diagnose.id==diagnoseId,Diagnose.status!=DiagnoseStatus.Del).first()
    @classmethod
    def addAdminIdAndChangeStatus(cls,diagnoseId,adminId):
        if adminId:
            return
        if mutex.acquire(1):
            try:
                diagnose=Diagnose.getDiagnoseById(diagnoseId)
                if diagnose.adminId is None:
                    diagnose.adminId=adminId
                    diagnose.status=DiagnoseStatus.Triaging
                    return session.commit()
            except Exception,e:
                print e.message
                return
            finally:
                mutex.release()
    @classmethod
    def changeDiagnoseStatus(cls,diagnoseId,status):
        if diagnoseId and status:
            diagnose=Diagnose.getDiagnoseById(diagnoseId)
            if diagnose:
                diagnose.status=status
                session.commit()
                session.flush()



    @classmethod
    def getDiagnosesByDoctorId(cls,session,doctorId,pagger,status=None,startTime=SystemTimeLimiter.startTime,endTime=SystemTimeLimiter.endTime):
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
            return session.query(Diagnose).filter(Diagnose.id==diagnoseId,Diagnose.status!=DiagnoseStatus.Del).first()

    @classmethod
    def getDiagnosesCountByAdmin(cls,session ,status=None,adminId=None,startTime=SystemTimeLimiter.startTime,endTime=SystemTimeLimiter.endTime):
        query=session.query(Diagnose)
        if status:
            query.filter(Diagnose.status==status)
        if adminId:
            query.filter(Diagnose.adminId==adminId)
        query.filter(Diagnose.createDate>startTime,Diagnose.createDate<endTime)
        return query.count()
    @classmethod
    def getDiagnosesByAdmin(cls,session,pagger ,status=None,adminId=None,startTime=SystemTimeLimiter.startTime,endTime=SystemTimeLimiter.endTime):

            if adminId is None:
                return
            query=session.query(Diagnose).filter(Diagnose.adminId==adminId)
            # count=Diagnose.getDiagnosesCountByAdmin(session,status,startTime,endTime)
            # pagger.count=count
            if status:
                query=query.filter(Diagnose.status==status)

            query=query.filter(Diagnose.createDate>startTime,Diagnose.createDate<endTime)
            return query.offset(pagger.getOffset()).limit(pagger.getLimitCount()).all()

    @classmethod
    def getDiagnoseByAdmin2(cls,session,hostpitalList=None,doctorName=None,pagger=Pagger(1,20) ):
        if doctorName is None and hostpitalList is None:
            return session.query(Diagnose).filter(Diagnose.status==DiagnoseStatus.NeedTriage).offset(pagger.getOffset()).limit(pagger.getLimitCount()).all()
        if doctorName is None:
            return session.query(Diagnose).filter(Diagnose.hospitalId.in_(hostpitalList),Diagnose.status==DiagnoseStatus.NeedTriage).offset(pagger.getOffset()).limit(pagger.getLimitCount()).all()

        if hostpitalList:
            query=session.query(Diagnose).select_from(join(Doctor,Diagnose,Doctor.id==Diagnose.doctorId))\
            .filter(Doctor.username==doctorName,Diagnose.status==DiagnoseStatus.NeedTriage,Diagnose.hospitalId.in_(hostpitalList)).offset(pagger.getOffset()).limit(pagger.getLimitCount())
        else:
            query=session.query(Diagnose).select_from(join(Doctor,Diagnose,Doctor.id==Diagnose.doctorId)) \
                .filter(Doctor.username==doctorName,Diagnose.status==DiagnoseStatus.NeedTriage).offset(pagger.getOffset()).limit(pagger.getLimitCount())
        return query.all()

class DiagnoseLog(Base):
    __tablename__ = 'diagnoseLog'
    __table_args__ = {
        'mysql_charset': 'utf8',
    }

    id = sa.Column(sa.Integer, primary_key = True, autoincrement = True)
    userId = sa.Column(sa.Integer)
    diagnoseId=sa.Column(sa.Integer)
    action=sa.Column(sa.String(128))
    createTime=sa.Column(sa.DateTime)
    def __init__(self,userId,diagnoseId,action):
        self.userId=userId
        self.diagnoseId=diagnoseId
        self.action=action
        self.createTime=datetime.now()

    @classmethod
    def save(cls,session,diagnoseLog):
        if diagnoseLog:
            session.add(diagnoseLog)
            session.commit()
            session.flush()
    @classmethod
    def getDiagnoseLogByDiagnoseId(cls,session,diagnoseId):
        if diagnoseId:
            return session.query(DiagnoseLog).filter(DiagnoseLog.diagnoseId==diagnoseId).order_by(DiagnoseLog.createTime).all()


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

class File(Base):
    __tablename__ = 'file'
    __table_args__ = {
        'mysql_charset': 'utf8',
        }

    id = sa.Column(sa.Integer, primary_key = True, autoincrement = True)
    type = sa.Column(sa.Integer)
    status=sa.Column(sa.Integer)
    url=sa.Column(sa.String(128))
    pathologyId=sa.Column(sa.Integer)


    def __init__(self,type,statues,url,pathologyId):
        self.type=type
        self.status=statues
        self.url=url
        self.pathologyId=pathologyId

    @classmethod
    def save(cls,dsFile):
        if dsFile is None:
            return
        session.add(File)
        session.commit()
    @classmethod
    def getFiles(cls,pathologyId,type=constant.FileType.Dicom):
        if pathologyId:
            if type:
                return session.query(File).filter(File.pathologyId==pathologyId,File.type==type,File.status==ModelStatus.Normal).all()
            else:
                return session.query(File).filter(File.pathologyId==pathologyId,File.status==ModelStatus.Normal).all()
    @classmethod
    def getDicomFileUrl(cls,pathologyId):
        if pathologyId:
            return session.query(File.url).filter(File.pathologyId==pathologyId,File.type==constant.FileType.Dicom,File.status==ModelStatus.Normal).first()

    @classmethod
    def getFilesUrl(cls,pathologyId):
        if pathologyId:
            return session.query(File.url).filter(File.pathologyId==pathologyId,File.type==constant.FileType.FileAboutDiagnose,File.status==ModelStatus.Normal).all()






