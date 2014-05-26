# coding: utf-8
__author__ = 'Jeremy'
from wtforms import Form, TextField, PasswordField, DateField, IntegerField, SelectField, BooleanField
from wtforms.validators import Required, Email, EqualTo, Length
from DoctorSpring.util.result_status import *

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

class ReportForm(object):
    reportId =None
    status=None
    techDesc =None
    imageDesc =None
    diagnoseDesc=None
    def __init__(self,args):
        if args.has('reportId'):
            self.reportId=args.get('reportId')

        self.status=args.get('status')
        self.techDesc=args.get('techDesc')
        self.imageDesc=args.get('imageDesc')
        self.diagnoseDesc=args.get('diagnoseDesc')
    def validate(self):
        try:
            if self.reportId is None:
                return FAILURE
            if self.status is None:
                return FAILURE

        except Exception,e:
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
        if args.has('doctorId'):
            self.doctorId=args.get('doctorId')

        if args.has('hospitalId'):
            self.hospitalId=args.get('hospitalId')
        if args.has('docId'):
            self.docId=args.get('docId')
    def validate(self):
        try:
            if self.userId is None:
                return FAILURE
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

