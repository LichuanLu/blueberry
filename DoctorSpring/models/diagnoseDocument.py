# coding: utf-8
__author__ = 'chengc017'

import sqlalchemy as sa
from  sqlalchemy import distinct

from database import Base
from sqlalchemy.orm import  relationship,backref,join
from patient import Patient

__author__ = 'chengc017'

import sqlalchemy as sa
from datetime import *
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
        'mysql_engine': 'MyISAM',
    }

    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    patientId = sa.Column(sa.Integer, sa.ForeignKey('patient.id'))
    patient = relationship("Patient", backref=backref('diagnose', order_by=id))
    diagnoseSeriesNumber = sa.Column(sa.String(256))


    doctorId = sa.Column(sa.Integer, sa.ForeignKey('doctor.id'))
    doctor = relationship("Doctor", backref=backref('diagnose', order_by=id))

    #adminId = sa.Column(sa.INTEGER,sa.ForeignKey('User.id'))
    #administrator = relationship("User", backref=backref('diagnose', order_by=id))
    adminId = sa.Column(sa.INTEGER)

    uploadUserId = sa.Column(sa.Integer, sa.ForeignKey('user.id'))
    uploadUser = relationship("User", backref=backref('diagnose', order_by=id))

    ossUploaded= sa.Column(sa.SmallInteger)

    pathologyId = sa.Column(sa.Integer, sa.ForeignKey('pathology.id'))
    pathology = relationship("Pathology", backref=backref('diagnose', order_by=id))

    reportId = sa.Column(sa.Integer, sa.ForeignKey('report.id'))
    report = relationship("Report", backref=backref('report', order_by=id))

    score = sa.Column(sa.Integer)

    createDate = sa.Column(sa.DateTime)
    reviewDate = sa.Column(sa.DATETIME)

    hospitalId = sa.Column(sa.Integer,sa.ForeignKey('hospital.id'))  #医院ID，用于医院批量提交诊断信息
    hospital = relationship("Hospital", backref=backref('diagnose', order_by=id))

    status = sa.Column(sa.INTEGER)      # 草稿：9， 成稿 1
    serveAdmin=sa.Column(sa.INTEGER) #产生aplpaly的管理员
    isConfirmOrder=sa.Column(sa.SmallInteger)#是否已经产生了阿里的订单

    def __init__(self,createdate=date.today()):
        self.createDate = createdate


    @classmethod
    def save(cls, diagnose):
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
        if adminId is None:
            return
        if mutex.acquire(1):
            try:
                diagnose=Diagnose.getDiagnoseById(diagnoseId)
                if diagnose.adminId is None or diagnose.adminId==0:
                    diagnose.adminId=adminId
                    diagnose.status=DiagnoseStatus.Triaging
                    session.commit()
                    return True
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
    def setDiagnoseUploaded(cls,diagnoseId):
        if diagnoseId :
            diagnose=session.query(Diagnose).filter(Diagnose.id==diagnoseId,Diagnose.status!=DiagnoseStatus.Del).first()
            if diagnose:
                diagnose.ossUploaded=constant.DiagnoseUploaed.Uploaded
                session.commit()
                session.flush()



    @classmethod
    def getDiagnosesByDoctorId(cls,session,doctorId,pagger,status=None,startTime=SystemTimeLimiter.startTime,endTime=SystemTimeLimiter.endTime):
        # count=Diagnose.getDiagnoseCountByDoctorId(doctorId,status,startTime,endTime)
        # pagger.count=count
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
                return session.query(Diagnose.id).filter(Diagnose.doctorId==doctorId,Diagnose.status==status,
                                                      Diagnose.createDate>startTime,Diagnose.createDate<endTime).count()
            else:
                return session.query(Diagnose.id).filter(Diagnose.doctorId==doctorId,Diagnose.status!=DiagnoseStatus.Del,
                                                      Diagnose.createDate>startTime,Diagnose.createDate<endTime).count()
    @classmethod
    def getNewDiagnoseCountByDoctorId(cls,doctorId):
        if doctorId:
            return session.query(Diagnose.id).filter(Diagnose.doctorId==doctorId,Diagnose.status==DiagnoseStatus.NeedDiagnose).count()
    @classmethod
    def getNewDiagnoseCountByUserId(cls,userID):
        if userID:
            query=session.query(Diagnose.id).join((Patient,Diagnose.patientId==Patient.id)).filter(Patient.userID==userID,Diagnose.status==DiagnoseStatus.Draft)
            return query.count()
    @classmethod
    def getNewDiagnoseByStatus(cls, status, userId):
        if status and userId:
            return session.query(Diagnose).filter(Diagnose.uploadUserId == userId, Diagnose.status == status).first()


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
    def getDiagnoseByDiagnoseSeriesNo(cls,diagnoseSeriesNo):
        if diagnoseSeriesNo:
            return session.query(Diagnose).filter(Diagnose.diagnoseSeriesNumber==diagnoseSeriesNo,Diagnose.status!=DiagnoseStatus.Del).first()
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
                if status==-1:
                    query=query.filter(Diagnose.status!=constant.DiagnoseStatus.Triaging)
                else:
                    query=query.filter(Diagnose.status==status)

            query=query.filter(Diagnose.createDate>startTime,Diagnose.createDate<endTime)
            return query.offset(pagger.getOffset()).limit(pagger.getLimitCount()).all()

    @classmethod
    def getDiagnoseByAdmin2(cls,session,hostpitalList=None,doctorName=None,pagger=Pagger(1,20) ):
        if (doctorName is None or doctorName == u'')and hostpitalList is None:
            return session.query(Diagnose).filter(Diagnose.status==DiagnoseStatus.NeedTriage).offset(pagger.getOffset()).limit(pagger.getLimitCount()).all()
        if doctorName is None or doctorName == u'':
            return session.query(Diagnose).filter(Diagnose.hospitalId.in_(hostpitalList),Diagnose.status==DiagnoseStatus.NeedTriage).offset(pagger.getOffset()).limit(pagger.getLimitCount()).all()

        if hostpitalList:
            query=session.query(Diagnose).select_from(join(Doctor,Diagnose,Doctor.id==Diagnose.doctorId))\
            .filter(Doctor.username==doctorName,Diagnose.status==DiagnoseStatus.NeedTriage,Diagnose.hospitalId.in_(hostpitalList)).offset(pagger.getOffset()).limit(pagger.getLimitCount())
        else:
            query=session.query(Diagnose).select_from(join(Doctor,Diagnose,Doctor.id==Diagnose.doctorId)) \
                .filter(Doctor.username==doctorName,Diagnose.status==DiagnoseStatus.NeedTriage).offset(pagger.getOffset()).limit(pagger.getLimitCount())
        return query.all()

    @classmethod
    def getNeedDealDiagnoseByHospitalUser(cls,session,uploadUserId,patientName=None,pagger=Pagger(1,20) ):
        if uploadUserId is None :
            return
        if patientName is None or patientName == u'':
            query=session.query(Diagnose)\
                .filter(Diagnose.uploadUserId==uploadUserId,Diagnose.status.in_((DiagnoseStatus.NeedTriage,DiagnoseStatus.NeedUpdate))).offset(pagger.getOffset()).limit(pagger.getLimitCount())
        else:
            query=session.query(Diagnose).select_from(join(Patient,Diagnose,Patient.id==Diagnose.patientId)) \
                .filter(Patient.realname==patientName,Diagnose.status.in_((DiagnoseStatus.NeedTriage,DiagnoseStatus.NeedUpdate)),Diagnose.uploadUserId==uploadUserId).offset(pagger.getOffset()).limit(pagger.getLimitCount())

        return query.all()

    @classmethod
    def getDiagnoseByPatientUser(cls,session,userId,status=None,pagger=Pagger(1,20) ):
        if userId is None :
            return
        query=None
        if status is None or len(status) == 0:
            query=session.query(Diagnose).select_from(join(Patient,Diagnose,Patient.id==Diagnose.patientId)) \
                .filter(Patient.userID==userId,Diagnose.status!=DiagnoseStatus.Del).offset(pagger.getOffset()).limit(pagger.getLimitCount())

        else:
            query=session.query(Diagnose).select_from(join(Patient,Diagnose,Patient.id==Diagnose.patientId)) \
                .filter(Patient.userID==userId,Diagnose.status==status).offset(pagger.getOffset()).limit(pagger.getLimitCount())


        return query.all()
    @classmethod
    def getDealedDiagnoseByHospitalUser(cls,session,uploadUserId,patientName,status,startTime,endTime,pagger=Pagger(1,20) ):
        if uploadUserId is None :
            return
        query=None
        if patientName is None or patientName == u'':
            query=session.query(Diagnose) \
                .filter(Diagnose.uploadUserId==uploadUserId,Diagnose.createDate>startTime,Diagnose.createDate<endTime)
        else:
            query=session.query(Diagnose).select_from(join(Patient,Diagnose,Patient.id==Diagnose.patientId)) \
                .filter(Diagnose.uploadUserId==uploadUserId,Diagnose.createDate>startTime,Diagnose.createDate<endTime,Patient.realname==patientName)


        if status==-1:
            query=query.filter(Diagnose.status.notin_((DiagnoseStatus.Diagnosed,DiagnoseStatus.Del)))

        elif status is None:
            query=query.filter(Diagnose.status!=DiagnoseStatus.Del)
        else:
            query=query.filter(Diagnose.status==DiagnoseStatus.Diagnosed)
        query=query.offset(pagger.getOffset()).limit(pagger.getLimitCount())
        return query.all()

    @classmethod
    def getDiagnoseCountByDoctorId(cls,session,doctorId,score=None):
        if doctorId is None:
            return
        if score or score==0:
            return session.query(Diagnose.id).filter(Diagnose.doctorId==doctorId,Diagnose.score==score).count()
        else:
            return  session.query(Diagnose.id).filter(Diagnose.doctorId==doctorId).count()


class DiagnoseLog(Base):
    __tablename__ = 'diagnoseLog'
    __table_args__ = {
        'mysql_charset': 'utf8',
        'mysql_engine': 'MyISAM',

    }

    id = sa.Column(sa.Integer, primary_key = True, autoincrement = True)
    userId = sa.Column(sa.Integer,sa.ForeignKey('user.id'))
    user = relationship("User", backref=backref('diagnoseLog', order_by=id))
    diagnoseId=sa.Column(sa.Integer)
    action=sa.Column(sa.String(128))
    description=sa.Column(sa.String(624))
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
    @classmethod
    def getDiagnoseLogByUserId(cls,userId):
        if userId:
            return session.query(DiagnoseLog).filter(DiagnoseLog.userId==userId).order_by(DiagnoseLog.createTime).all()


class DiagnoseTemplate(Base):
    __tablename__ = 'diagnosetemplate'
    __table_args__ = {
        'mysql_charset': 'utf8',
        'mysql_engine': 'MyISAM',
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
            results =session.query(DiagnoseTemplate.diagnosePosition,DiagnoseTemplate.diagnoseDesc,
                                 DiagnoseTemplate.imageDesc).filter(DiagnoseTemplate.diagnoseMethod==diagnoseMethod,
                                                                           DiagnoseTemplate.diagnosePosition==diagnosePosition) \
                .group_by(DiagnoseTemplate.diagnoseDesc).all()
            if results and len(results)>0:
                resultsDict=[]
                for result in results:
                    resultDict={}
                    resultDict['diagnosePosition']=result[0]
                    resultDict['diagnoseDesc']=result[1]
                    resultDict['imageDesc']=result[2]
                    resultsDict.append(resultDict)
                return resultsDict






class Report(Base):
    __tablename__ = 'report'
    __table_args__ = {
        'mysql_charset': 'utf8',
        'mysql_engine': 'MyISAM',
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
        if maxId is None:
            maxId=1
        self.seriesNumber='%s%i'%(SeriesNumberPrefix,SeriesNumberBase+maxId[0]+1)
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
            if type or type==0:
                report.type=type
            if status or status==0:
                report.status=status
            if fileUrl:
                report.fileUrl=fileUrl
            if techDesc:
                report.techDesc=techDesc
            if imageDesc:
                report.imageDesc=imageDesc
            if diagnoseDesc:
                report.diagnoseDesc=diagnoseDesc

            session.flush()
            session.commit()
        return report

class File(Base):
    __tablename__ = 'file'
    __table_args__ = {
        'mysql_charset': 'utf8',
        'mysql_engine': 'MyISAM',
    }

    id = sa.Column(sa.Integer, primary_key = True, autoincrement = True)
    name = sa.Column(sa.String(128))
    type = sa.Column(sa.Integer) # 1.dicom 2.诊断书
    size = sa.Column(sa.String(32))
    status=sa.Column(sa.Integer)
    url=sa.Column(sa.String(128))
    pathologyId=sa.Column(sa.Integer)


    def __init__(self,type,name,size,url):
        self.type = type
        self.name = name
        self.size = size
        self.status = ModelStatus.Normal
        self.url = url

    @classmethod
    def save(cls,dsFile):
        if dsFile:
            session.add(dsFile)
            session.commit()
            session.flush()

    @classmethod
    def getFiles(cls,pathologyId,type=constant.FileType.Dicom):
        if pathologyId:
            return session.query(File).filter(File.pathologyId==pathologyId,File.type==type,File.status==ModelStatus.Normal).all()

    @classmethod
    def getFilebyId(cls, id):
        if id:
            return session.query(File).filter(File.id == id, File.status==ModelStatus.Normal).first()

    @classmethod
    def getFilebypathologyId(cls, pathologyId, type=None):
        if pathologyId:
            query = session.query(File).filter(File.pathologyId == pathologyId, File.status==ModelStatus.Normal)
            if type is not None:
                query = query.filter(File.type == type)

            return query.all()

    @classmethod
    def getDicomFileUrl(cls,pathologyId):
        if pathologyId:
            return session.query(File.url).filter(File.pathologyId==pathologyId,File.type==constant.FileType.Dicom,File.status==ModelStatus.Normal).first()

    @classmethod
    def getFilesUrl(cls,pathologyId):
        if pathologyId:
            return session.query(File.url).filter(File.pathologyId==pathologyId,File.type==constant.FileType.FileAboutDiagnose,File.status==ModelStatus.Normal).all()


    @classmethod
    def cleanDirtyFile(cls, fileIds, pathologyId, type):
        if fileIds is not None and len(fileIds) > 0 and pathologyId:
            files = File.getFilebypathologyId(pathologyId, type)
            for file in files:
                if not unicode(file.id) in fileIds:
                        file.status = ModelStatus.Del



