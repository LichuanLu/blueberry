# coding: utf-8
__author__ = 'ccheng'

from flask import Flask, request, session, g, redirect, url_for, Blueprint, jsonify
from flask import abort, render_template, flash
from flask.ext.login import login_user, logout_user, current_user, login_required
from forms import LoginForm, RegisterForm ,CommentsForm ,MessageForm
from DoctorSpring import lm
from database import  db_session
from sqlalchemy.exc import IntegrityError
from DoctorSpring.models import User,Patent,Doctor,Diagnose ,DiagnoseTemplate
from DoctorSpring.models import User,Comment,Message
from DoctorSpring.util import result_status as rs,object2dict
from DoctorSpring.util.constant import MessageUserType,Pagger

import  data_change_service as dataChangeService
import json

import config
config = config.rec()

uc = Blueprint('user_center', __name__)


@uc.route('/doctor/<int:doctorId>/home',  methods = ['GET', 'POST'])
def endterDoctorHome(doctorId):

    doctor=Doctor.getById(doctorId)
    if doctor is None:
        return redirect(url_for('/300'))

    resultDate={}
    messageCount=Message.getMessageCountByReceiver(doctorId)
    resultDate['messageCount']=messageCount

    diagnoseCount=Diagnose.getNewDiagnoseCountByDoctorId(doctorId)
    resultDate['diagnoseCount']=diagnoseCount

    resultDate['doctor']=doctor
    pager=Pagger(1,20)
    diagnoses=Diagnose.getDiagnosesByDoctorId(doctorId,pager)
    diagnoseDict=dataChangeService.userCenterDiagnoses(diagnoses)
    resultDate['diagnoses']=diagnoseDict
    return render_template("doctorHome.html",data=resultDate)

@uc.route('/doctor/<int:doctorId>/patientList',  methods = ['GET', 'POST'])
def getPatients(doctorId):
     patients=Diagnose.getPatientListByDoctorId(doctorId)
     patientsDict=object2dict.objects2dicts(patients)
     resultStatus=rs.ResultStatus(rs.SUCCESS.status,rs.SUCCESS.msg,patientsDict)
     resultDict=resultStatus.__dict__
     return json.dumps(resultDict,ensure_ascii=False)
@uc.route('/diagnoseTemplate/postionList',  methods = ['GET', 'POST'])
def getPostionList():
    diagnoseMethod=request.args.get('diagnoseMethod')
    diagnosePositions=DiagnoseTemplate.getDiagnosePostion(diagnoseMethod)
    resultStatus=rs.ResultStatus(rs.SUCCESS.status,rs.SUCCESS.msg,diagnosePositions)
    resultDict=resultStatus.__dict__
    return json.dumps(resultDict,ensure_ascii=False)
@uc.route('/diagnoseTemplate/diagnoseAndImageDesc',  methods = ['GET', 'POST'])
def getDiagnoseAndImageDescList():
    diagnoseMethod=request.args.get('diagnoseMethod')
    diagnosePostion=request.args.get('diagnosePostion')
    diagnoseAndImageDescs=DiagnoseTemplate.getDiagnoseAndImageDescs(diagnoseMethod,diagnosePostion)
    resultStatus=rs.ResultStatus(rs.SUCCESS.status,rs.SUCCESS.msg,diagnoseAndImageDescs)
    resultDict=resultStatus.__dict__
    return json.dumps(resultDict,ensure_ascii=False)