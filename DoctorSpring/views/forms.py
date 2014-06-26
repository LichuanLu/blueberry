# coding: utf-8
__author__ = 'Jeremy'
from wtforms import Form, TextField, PasswordField, DateField, IntegerField, SelectField, BooleanField
from wtforms.validators import Required, Email, EqualTo, Length
from DoctorSpring.util.result_status import *
from DoctorSpring.models import User, Patient, Doctor ,Diagnose
import string

class RegisterForm(Form):
    name = TextField('Username', validators=[Required(), Length(min=3, max=25)])
    #email = TextField('Email', validators=[Required(), Length(min=6, max=40)])
    password = PasswordField('Password',
                             validators=[Required(), Length(min=6, max=40)])
    # confirm = PasswordField(
    #     'Repeat Password',
    #     [Required(), EqualTo('password', message='Passwords must match')])

class DiagnoseForm1(Form):
    patientid = None
    patientname = None
    patientsex = None
    birthdate = None
    identitynumber = None
    phonenumber = None
    location = None
    def __init__(self, args):
        self.patientid = args.get('patientId')
        self.patientname = args.get('patientname')
        self.patientsex = args.get('patientsex')
        self.birthdate = args.get('birthdate')
        self.identitynumber = args.get('identitynumber')
        self.phonenumber = args.get('phonenumber')
        self.location = args.get('location')
    def validate(self):
        try:
            if self.patientid is not None:
                return SUCCESS
            if self.patientname is None:
                failure = ResultStatus(FAILURE.status, "请填写就诊人姓名")
                return failure
            if self.patientsex is None:
                failure = ResultStatus(FAILURE.status, "请选择性别")
                return failure
            if self.birthdate is None:
                failure = ResultStatus(FAILURE.status, "请选择出生日期")
                return failure
            if self.identitynumber is None:
                failure = ResultStatus(FAILURE.status, "请填写身份证号")
                return failure
            if self.phonenumber is None:
                failure = ResultStatus(FAILURE.status, "请填写手机号码")
                return failure
            if self.location is None:
                failure = ResultStatus(FAILURE.status, "请选择所在地")
                return failure
        except Exception, e:
            return FAILURE
        return SUCCESS

class DiagnoseForm3(Form):
    doctorId = None
    def __init__(self, args):
        self.doctorId = args.get('doctorId')
    def validate(self):
        try:
            if self.doctorId is None:
                failure = ResultStatus(FAILURE.status, "请选择医生")
                return failure
        except Exception, e:
            return FAILURE
        return SUCCESS

class DiagnoseForm2(Form):
    # patientlocation=1&patientlocation=2&dicomtype=1&fileurl=http%3A%2F%2F127.0.0.1%3A5000%2Fstatic%2Ftmp%2Flogin.html
    patientlocation = None
    dicomtype = None
    fileurl = None
    def __init__(self, args):
        self.patientlocation = args.get('patientlocation')
        self.dicomtype = int(args.get('dicomtype'))
        self.fileurl = args.get('fileurl')
    def validate(self):
        try:
            if self.patientlocation is None:
                failure = ResultStatus(FAILURE.status, "请选择就诊部位")
                return failure
            if self.dicomtype is None:
                failure = ResultStatus(FAILURE.status, "请选择影像类型")
                return failure
            if self.fileurl is None:
                failure = ResultStatus(FAILURE.status, "请上传有效的影音文件")
                return failure
        except Exception, e:
            return FAILURE
        return SUCCESS

class DiagnoseForm4(Form):
    # diagnoseHistory=zzzzzzz&illnessHistory=%E5%8F%91%E7%9F%AD%E5%8F%91%E7%9F%AD%E5%8F%91%E6%88%91%E8%84%9A%E6%89%8B%E6%9E%B6%E6%88%91%E5%8F%AB%E6%88%91%E9%87%91%E9%A2%9D%E5%93%A6%E6%94%BE%E5%81%87%E6%88%91%E5%B0%B1
    diagnoseHistory = None
    illnessHistory = None
    fileurl = None
    def __init__(self, args):
        self.diagnoseHistory = args.get('diagnoseHistory')
        self.illnessHistory = args.get('illnessHistory')
        self.fileurl = args.get('fileurl')
    def validate(self):
        try:
            if self.patientlocation is None:
                failure = ResultStatus(FAILURE.status, "请选择就诊部位")
                return failure
            if self.dicomtype is None:
                failure = ResultStatus(FAILURE.status, "请选择影像类型")
                return failure
                # if self.fileurl is None:
                #     failure = ResultStatus(FAILURE.status, "请上传有效的影音文件")
                #     return failure
        except Exception, e:
            return FAILURE
        return SUCCESS


class CommentsForm(object):
    userId =None
    receiverId=None
    content = None
    title = None
    diagnoseId=None
    score=None
    def __init__(self,args):
        self.content=args.get('content')
        self.diagnoseId=args.get('diagnoseId')
        self.score=args.get('score')

    def validate(self):
        try:
            if self.diagnoseId is None:
                return FAILURE
            diagnose=Diagnose.getDiagnoseById(self.diagnoseId)
            if diagnose is None:
                return FAILURE
            if diagnose.doctorId and hasattr(diagnose,'doctor') and diagnose.doctor and diagnose.doctor.userId:
                self.receiverId=diagnose.doctor.userId
            else:
                return FAILURE
            if diagnose.patientId and hasattr(diagnose,'patient') and diagnose.patient and diagnose.patient.userID:
                self.userId=diagnose.patient.userID
            else:
                return FAILURE
            # if self.title is None:
            #     return FAILURE
            if self.content is None or len(self.content)<10:
                failure=ResultStatus(FAILURE.status,"输入的内容长度必须大于等于10")
                return  failure
            if self.score is None or self.score == u'':
                return FAILURE
            else:
                self.score=string.atoi(self.score)
        except Exception,e:
            return FAILURE
        return SUCCESS

class MessageForm(Form):
    senderId = IntegerField('senderId', validators=[Required()])
    receiverId=IntegerField('receiverId', validators=[Required()])
    content = TextField('content', validators=[Required()])
    title = TextField('title')
    type=IntegerField('type', validators=[Required()])

class ConsultForm(object):
    userId =None
    doctorId=None
    content =None
    title =None
    def __init__(self,args):
        self.userId=args.get('userId')
        self.doctorId=args.get('doctorId')
        self.title=args.get('title')
        self.content=args.get('content')
    def validate(self):
        try:
            if self.userId is None:
                return FAILURE
            if self.doctorId is None:
                return FAILURE
            if self.title is None:
                return FAILURE
            if self.content is None or len(self.content)<10:
                failure=ResultStatus(FAILURE.status,"输入的内容长度必须大于等于10")
                return  failure
        except Exception,e:
            return FAILURE
        return SUCCESS

class LoginForm(object):
    username = None
    password = None
    remember_me = None
    def __init__(self, args):
        self.username=args.get('name')
        self.password=args.get('pass')
        #self.remember_me=args.get('remember_me')
    def validate(self):
        try:
            if self.username is None:
                failure = ResultStatus(FAILURE.status, "用户名为空")
                return failure
            if self.password is None:
                failure=ResultStatus(FAILURE.status, "密码为空")
                return failure
        except Exception,e:
            return FAILURE
        return SUCCESS

class ReportForm(object):
    reportId =None
    status=None
    techDesc =None
    imageDesc =None
    diagnoseDesc=None
    diagnoseId=None
    fileUrl=None
    def __init__(self,args):
        #if args.has('reportId'):
        self.reportId=args.get('reportId')

        self.status=args.get('status')
        if self.status:
            self.status=string.atoi(self.status)
        self.techDesc=args.get('techDesc')
        self.imageDesc=args.get('imageDesc')
        self.diagnoseDesc=args.get('diagnoseDesc')
        self.diagnoseId=args.get('diagnoseId')
        if self.diagnoseId:
            self.diagnoseId=string.atoi(self.diagnoseId)
        self.fileUrl=args.get('fileUrl')
    def validate(self):
        try:
            if self.diagnoseDesc is None:
                return FAILURE
            if self.imageDesc is None:
                return FAILURE
            if self.diagnoseId is None:
                return FAILURE

        except Exception,e:
            return FAILURE
        return SUCCESS


class RegisterFormPatent(object):
    name = None
    password = None
    def __init__(self, args):
        self.name = args.get('name')
        self.password = args.get('password')


    def validate(self):
        try:
            if self.password is None:
                failure = ResultStatus(FAILURE.status, "密码为空")
                return failure
            if self.name is None:
                failure = ResultStatus(FAILURE.status, "用户名为空")
                return failure
            else:
                user = User.get_by_name(self.name)
                if user is not None:
                    failure = ResultStatus(FAILURE.status, "该用户已存在")
                    return failure
        except Exception, e:
            return FAILURE
        return SUCCESS



class UserFavortiesForm(object):
    userId =None
    doctorId=None
    hospitalId =None
    docId =None
    type=None
    def __init__(self,args):


        self.userId=args.get('userId')
        self.type=args.get('type')
        #if args.has('doctorId'):
        self.doctorId=args.get('doctorId')
        #if args.has('hospitalId'):
        self.hospitalId=args.get('hospitalId')
        #if args.has('docId'):
        self.docId=args.get('docId')
        #if args.has('doctorId'):
        self.doctorId=args.get('doctorId')

        #if args.has('hospitalId'):
        self.hospitalId=args.get('hospitalId')
        #if args.has('docId'):
        self.docId=args.get('docId')
    def validate(self):
        try:

            if self.type is None:
                return FAILURE
            if self.docId is None and self.hospitalId is None and self.doctorId is None:
                return FAILURE

        except Exception,e:
            return FAILURE
        return SUCCESS

class PatientUpdateForm(object):
    userId=None
    patientId=None
    name=None
    account=None
    mobile=None
    address=None
    email=None
    identityCode=None
    yibaoCard=None

class RegisterFormDoctor(object):
    email = None
    username = None
    password = None
    real_name = None
    identity_phone = None
    cellphone = None
    def __init__(self, args):
        self.email = args.get('email')
        self.username = args.get('username')
        self.password = args.get('password')
        self.real_name = args.get('realname')
        self.identity_phone = args.get('identityphone')
        self.cellphone = args.get('cellphone')
    def validate(self):
        try:
            if self.email is None or "@" not in self.email:
                failure = ResultStatus(FAILURE.status, "邮箱地址格式不正确")
                return failure
            else:
                user = User.get_by_name(self.email)
                if user is not None:
                    failure = ResultStatus(FAILURE.status, "邮箱地址已注册")
                    return failure
            if self.username is None:
                failure = ResultStatus(FAILURE.status, "用户名为空")
                return failure
            if self.password is None:
                failure = ResultStatus(FAILURE.status, "密码为空")
                return failure
            if self.real_name is None:
                failure = ResultStatus(FAILURE.status, "真实姓名为空")
                return failure
            if self.identity_phone is None:
                failure = ResultStatus(FAILURE.status, "注册号码为空")
                return failure
            if self.cellphone is None:
                failure = ResultStatus(FAILURE.status, "手机号码格式不对")
                return failure
            else:
                user = User.get_by_name(self.cellphone)
                if user is not None:
                    failure = ResultStatus(FAILURE.status, "手机号码已注册")
                    return failure
        except Exception, e:
            return FAILURE
        return SUCCESS
    
class ThanksNoteForm(object):
    userId =None
    receiver=None
    content =None
    title =None
    def __init__(self,args):
        self.receiver=args.get('receiver')

        self.title=args.get('title')
        self.content=args.get('content')
    def validate(self):
        try:

            if self.receiver is None:
                return FAILURE
            # if self.title is None:
            #     return FAILURE
            if self.content is None or len(self.content)<10:
                failure=ResultStatus(FAILURE.status,"输入的内容长度必须大于等于10")
                return  failure
        except Exception,e:
            return FAILURE
        return SUCCESS
        return SUCCESS

class DoctorList(Form):
    # /doctors/list.json?hospitalId=1&sectionId=0&doctorname=ddd&pageNumber=1&pageSize=6
    hospitalId = None
    sectionId = None
    doctorname = None
    pageNumber = None
    pageSize = None
    def __init__(self, args):
        self.hospitalId = args.get('hospitalId')
        self.sectionId = args.get('sectionId')
        self.doctorname = args.get('doctorname')
        self.pageNumber = args.get('pageNumber')
        self.pageSize = args.get('pageSize')
    def validate(self):
        if self.hospitalId is None:
            self.hospitalId = 0
        if self.sectionId is None:
            self.sectionId = 0
        if self.doctorname is None:
            self.doctorname = ''
        if self.pageNumber is None:
            self.pageNumber = 1
        if self.pageSize is None:
            self.pageSize = 6
        return SUCCESS
