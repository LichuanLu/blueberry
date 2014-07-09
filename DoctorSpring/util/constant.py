# coding: utf-8
__author__ = 'chengc017'
from datetime import  datetime
import config
import string
class ModelStatus(object):
      Normal=0
      Del=1
      Draft=9   #草稿



class UserStatus(object):
    patent = 0  # 普通用户
    doctor = 1  # 医生账户

class PatientStatus(object):
    patent = 0  # 普通注册用户
    diagnose = 1  # 病例用户


# class DiagnoseMetaStatus(object):
#     def __init__(self,status,statusName):
#1. 草稿 2.待付费 3. 待分诊 4. 分诊中 5. 待诊断 6. 诊断完成 7.需要更新信息 8. 无法诊断
class DiagnoseStatus(object):
    Draft=9 #草稿
    Del=1 #删除
    NeedPay=2
    NeedTriage=3 #待分诊
    Triaging=4   #分诊中
    NeedDiagnose=5 #待诊断
    Diagnosed=6 #诊断完成
    NeedUpdate=7 #需要更新信息
    UnableDiagnose=8#无法诊断
    @staticmethod
    def getStatusName(status):
        if status==DiagnoseStatus.Draft:
            return '草稿'
        if status==DiagnoseStatus.NeedPay:
            return '待交费'
        if status==DiagnoseStatus.NeedTriage:
            return '待分诊'
        if status==DiagnoseStatus.Triaging:
            return '分诊中'
        if status==DiagnoseStatus.NeedDiagnose:
            return '待诊断'
        if status==DiagnoseStatus.Diagnosed:
            return '诊断完成'
        if status==DiagnoseStatus.NeedUpdate:
            return '需要更新信息'
        if status==DiagnoseStatus.UnableDiagnose:
            return '无法诊断'

class DiagnoseUploaed(object):
    NoUploaded=0
    Uploaded=1
class ReportStatus(object):
    Draft=0
    Del=1
    Commited=2
class ReportType(object):
    Admin=0
    Doctor=1

class FileType(object):
    Dicom=0
    FileAboutDiagnose=1   # 诊断书

SeriesNumberPrefix='YZD'
SeriesNumberBase=500000
DiagnoseSeriesNumberPrefix='DS'
DiagnoseSeriesNumberBase=50000

class MessageStatus(ModelStatus):
      Readed=2

class CommentType(object):
    DiagnoseComment=0
    Normal=1

class MessageType(object):
    Normal=0
    ThankNote=1
    System=2
    Diagnose=3
class MessageUserType(object):
    user=0
    hospitalUser=1
    patient=2
    doctor=3
class SystemTimeLimiter(object):
    startTime=datetime(2014,5,20)
    endTime=datetime(3014,5,20)
class Pagger(object):
    pageNo=1
    pageSize=20
    count=0
    def __init__(self,pageNo,pageSize):
        if pageNo:
            if isinstance(pageNo,basestring):
                self.pageNo=string.atoi(pageNo)
            else:
                self.pageNo=pageNo
        if pageSize:
            if isinstance(pageSize,basestring):
                self.pageSize=string.atoi(pageSize)
            else:
                self.pageSize=pageSize
        #self.count=count
    def getOffset(self):
        offset=(self.pageNo-1)*self.pageSize
        if offset<=self.count:
            return offset
    def getLimitCount(self):
        if self.count==0:
            return self.pageSize

        offset=(self.pageNo-1)*self.pageSize
        if offset+self.pageSize<=self.count:
            return self.pageSize
        else:
            return self.count-offset

class DirConstant(object):
    ROOT_DIR=config.ROOT_DIR
    DIAGNOSE_PDF_DIR=ROOT_DIR+'/DoctorSpring/static/pdf/'

class UserFavoritesType(object):
    Doctor=0
    Hospital=1
    Diagnose=2

DefaultSystemAdminUserId=1

class RoleId(object):
    Admin=1
    Doctor=2
    Patient=3
    HospitalUser=4
class DiagnoseLogAction(object):
    NewDiagnoseAction='提出诊断申请'
    FetchDiagnoseAction='正在分发诊断'
    FetchDiagnoseEndAction='分发诊断完成'
    TriageDiagnoseAction='正在进行诊断'
    UpateDiagnoseAction='正在进行诊断'
    DiagnoseNeedUpateAction='暂停分发诊断(需要更多就诊人信息)'
    DiagnoseFinished='完成诊断'
    CancleDiagnose='取消诊断'


DiagnoseScore={
    0:'不满意',
    1:'满意',
    2:'很满意',
}
Gender={
    1:'男',
    2:'女',
}
class DoctorProfileType(object):
    #简历：0  介绍：1 荣誉：2  其他：3
    Resume=0
    Intro=1
    Award=2
    Other=3
class DoctorType(object):
    Doctor=0
    HospitalUser=1








