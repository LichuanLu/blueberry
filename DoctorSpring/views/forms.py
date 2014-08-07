# coding: utf-8
__author__ = 'Jeremy'
from DoctorSpring.util.result_status import *
from DoctorSpring.models import User, Patient, Doctor ,Diagnose
import string

class DiagnoseForm1(object):
    patientid = None
    patientname = None
    patientsex = None
    birthdate = None
    identitynumber = None
    phonenumber = None
    locationId = None
    isHospitalUser = False
    exist = False
    diagnoseId = None
    def __init__(self, args):

        if 'type' in args.keys() and args.get('type') == 1:
            isHospitalUser = True

        if 'diagnoseId' in args.keys():
            self.diagnoseId = args.get('diagnoseId')

        if 'patientname' not in args.keys():
            self.exist = True
            self.patientid = args.get('patientId')
        else:
            self.patientid = args.get('patientId')
            self.patientname = args.get('patientname')
            self.patientsex = args.get('patientsex')
            self.birthdate = args.get('birthdate')
            self.identitynumber = args.get('identitynumber')
            self.phonenumber = args.get('phonenumber')
            self.locationId = args.get('locationId')
    def validate(self):
        try:
            if(self.exist):
                if self.patientid is not None:
                    return SUCCESS
            else:
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
                if self.locationId is None:
                    failure = ResultStatus(FAILURE.status, "请选择所在地")
                    return failure
        except Exception, e:
            return FAILURE
        return SUCCESS

class DiagnoseForm3(object):
    doctorId = None
    diagnoseId = None
    def __init__(self, args):
        self.diagnoseId = args.get('diagnoseId')
        self.doctorId = args.get('doctorId')
    def validate(self):
        try:
            if self.doctorId is None:
                failure = ResultStatus(FAILURE.status, "请选择医生")
                return failure
        except Exception, e:
            return FAILURE
        return SUCCESS

class DiagnoseForm2(object):
    # patientlocation=1&patientlocation=2&dicomtype=1&fileurl=http%3A%2F%2F127.0.0.1%3A5000%2Fstatic%2Ftmp%2Flogin.html
    patientlocation = None
    dicomtype = None
    fileurl = None
    pathologyId = None
    exist = False
    diagnoseId = None
    def __init__(self, args):
        if 'pathologyId' in args.keys():
            self.pathologyId = args.get('pathologyId')
            self.exist = True
        if 'diagnoseId' in args.keys():
            self.diagnoseId = args.get('diagnoseId')
        self.patientid = args.get('patientId')
        self.patientlocation = args.getlist('patientlocation')
        self.dicomtype = args.get('dicomtype')
        self.fileurl = [args.get('fileid')]

    def validate(self):
        try:
            if self.pathologyId is not None:
                return SUCCESS
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

class DiagnoseForm4(object):
    # diagnoseHistory=zzzzzzz&illnessHistory=%E5%8F%91%E7%9F%AD%E5%8F%91%E7%9F%AD%E5%8F%91%E6%88%91%E8%84%9A%E6%89%8B%E6%9E%B6%E6%88%91%E5%8F%AB%E6%88%91%E9%87%91%E9%A2%9D%E5%93%A6%E6%94%BE%E5%81%87%E6%88%91%E5%B0%B1
    hospitalId = None
    illnessHistory = None
    fileurl = None
    diagnoseId = None
    def __init__(self, args):
        if 'diagnoseId' in args.keys():
            self.diagnoseId = args.get('diagnoseId')
        self.hospitalId = int(args.get('hospitalId'))
        self.illnessHistory = args.get('illnessHistory')
        self.fileurl = args.getlist('fileid')
    def validate(self):
        try:
            if self.hospitalId is None:
                failure = ResultStatus(FAILURE.status, "请选择就诊医院")
                return failure
            if self.illnessHistory is None:
                failure = ResultStatus(FAILURE.status, "请填写病史信息")
                return failure
            if self.fileurl is None:
                failure = ResultStatus(FAILURE.status, "请上传有效的诊断书")
                return failure
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
        # self.nickname=args.get('nickname')
        self.username=args.get('name')
        self.password=args.get('password')
        #self.remember_me=args.get('remember_me')
    def validate(self):
        try:
            # if self.nickname is None:
            #     failure = ResultStatus(FAILURE.status, "昵称为空")
            #     return failure
            if self.username is None:
                failure = ResultStatus(FAILURE.status, "邮箱或手机为空")
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
        self.nickname = args.get('nickname')
        self.name = args.get('name')
        self.password = args.get('password')


    def validate(self):
        try:

            if self.nickname is None:
                failure = ResultStatus(FAILURE.status, "昵称为空")
                return failure
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

class UserUpdateForm(object):
    userId=None
    patientId=None
    nickName=None
    name=None
    account=None
    mobile=None
    address=None
    email=None
    identityCode=None
    yibaoCard=None
    def __init__(self,userForm):
        self.userId=userForm.get('userId')
        self.patientId=userForm.get('patientId')
        self.nickName=userForm.get('nickName')
        self.name=userForm.get('name')
        self.account=userForm.get('account')
        self.mobile=userForm.get('mobile')
        self.address=userForm.get('address')
        self.email=userForm.get('email')
        self.identityCode=userForm.get('identityCode')
        self.yibaoCard=userForm.get('yibaoCard')
    def validate(self):
        try:
            if self.email is None or "@" not in self.email:
                failure = ResultStatus(FAILURE.status, "邮箱地址格式不正确")
                return failure
            if self.account is None:
                failure = ResultStatus(FAILURE.status, "账号不能为空")
        except Exception, e:
            return FAILURE
        return SUCCESS
class UserChangePasswdForm(object) :
    userId = None
    oldPasswd = None
    newPasswd = None
    def __init__(self,form):
        self.oldPasswd=form.get('oldPasswd')
        self.newPasswd=form.get('newPasswd')
    def validate(self):
        if self.oldPasswd is None:
            return FAILURE
        if self.newPasswd is None or len(self.newPasswd)<6 or len(self.oldPasswd)>50:
            return ResultStatus(FAILURE.status,"输入的密码长度必须大于6小于50")
        return SUCCESS


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

class DoctorList(object):
    # /doctors/list.json?hospitalId=1&sectionId=0&doctorname=ddd&pageNumber=1&pageSize=6
    hospitalId = None
    sectionId = None
    doctorname = None
    pageNumber = None
    pageSize = None
    def __init__(self, request):
        args = request.args
        if 'doctorname' in args.keys():
            self.doctorname = str(args.get('doctorname'))
        self.hospitalId = args['hospitalId']
        self.sectionId = request.args['skillId']
        self.pageNumber = request.args['pageNumber']
        self.pageSize = request.args['pageSize']
    def validate(self):
        if self.hospitalId is None:
            self.hospitalId = -1
        if self.sectionId is None:
            self.sectionId = -1
        if self.doctorname is None:
            self.doctorname = ''
        if self.pageNumber is None:
            self.pageNumber = 1
        if self.pageSize is None:
            self.pageSize = 6
        return SUCCESS


class Dicominfo(object):
    hospitalId = None
    sectionId = None
    doctorname = None
    pageNumber = None
    pageSize = None