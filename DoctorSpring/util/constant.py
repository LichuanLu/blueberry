# coding: utf-8
__author__ = 'chengc017'
from datetime import  datetime
import config
class ModelStatus(object):
      Normal=0
      Del=1


class UserStatus(object):
    patent = 0  # 普通用户
    doctor = 1  # 医生账户

class PatientStatus(object):
    patent = 0  # 普通注册用户
    diagnose = 1  # 病例用户


#1. 草稿 2.待付费 3. 待分诊 4. 分诊中 5. 待诊断 6. 诊断完成 7.需要更新信息 8. 无法诊断
class DiagnoseStatus(object):
    Draft=0 #草稿
    Del=1 #删除
    NeedPay=2
    NeedTriage=3 #待分诊
    Triaging=4   #分诊中
    NeedDiagnose=5 #待诊断
    Diagnosed=6 #诊断完成
    NeedUpdate=7 #需要更新信息
    UnableDiagnose=8#无法诊断
class ReportStatus(object):
    Draft=0
    Del=1
    Commited=2
class ReportType(object):
    Admin=0
    Doctor=1

class FileType(object):
    Dicom=0
    FileAboutDiagnose=1
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
        self.pageNo=pageNo
        self.pageSize=pageSize
        #self.count=count
    def getOffset(self):
        offset=(self.pageNo-1)*self.pageSize
        if offset<=self.count:
            return offset
    def getLimitCount(self):
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




