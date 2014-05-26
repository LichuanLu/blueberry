# coding: utf-8
__author__ = 'Jeremy'
from wtforms import Form, TextField, PasswordField, DateField, IntegerField, SelectField, BooleanField
from wtforms.validators import Required, Email, EqualTo, Length
from DoctorSpring.util.result_status import *
from DoctorSpring.models import User, Patent, Doctor

class RegisterForm(Form):
    name = TextField('Username', validators=[Required(), Length(min=3, max=25)])
    #email = TextField('Email', validators=[Required(), Length(min=6, max=40)])
    password = PasswordField('Password',
                             validators=[Required(), Length(min=6, max=40)])
    # confirm = PasswordField(
    #     'Repeat Password',
    #     [Required(), EqualTo('password', message='Passwords must match')])

class LoginForm(Form):
    name = TextField('username', validators=[Required()])
    password = PasswordField('password', validators=[Required()])
    email = TextField('email')
    remember_me = BooleanField('remember_me', default = False)

class DiagnoseForm(Form):
    patientname = TextField('patientname')
    birthdate = TextField('birthdate')
    phonenumber = TextField('phonenumber')
    location = TextField('location')
    patientname = TextField('patientname')
    patientname = TextField('patientname')
    patientname = TextField('patientname')
    patientname = TextField('patientname')







class CommentsForm(Form):
    userId = IntegerField('userId', validators=[Required()])
    receiverId=IntegerField('receiverId', validators=[Required()])
    content = TextField('content', validators=[Required()])
    title = TextField('title')
    diagnoseId=IntegerField('diagnoseId')
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

class LoginForm1(object):
    Username =None
    Password=None
    remember_me =None
    def __init__(self,args):
        self.Username=args.get('Username')
        self.Password=args.get('Password')
        self.remember_me=args.get('remember_me')
    def validate(self):
        try:
            if self.Username is None or len(self.Username)<10:
                failure=ResultStatus(FAILURE.status,"用户名的长度必须大于等于10")
                return failure
            if self.Password is None or len(self.Password)<10:
                failure=ResultStatus(FAILURE.status,"密码的长度必须大于等于10")
                return failure
            if self.remember_me is None:
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