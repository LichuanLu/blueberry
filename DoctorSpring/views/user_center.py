# coding: utf-8
__author__ = 'ccheng'

from flask import Flask, request, session, g, redirect, url_for, Blueprint, jsonify
from flask import abort, render_template, flash
from flask.ext.login import login_user, logout_user, current_user, login_required
from forms import LoginForm, RegisterForm ,CommentsForm ,MessageForm ,UserFavortiesForm,ThanksNoteForm
from DoctorSpring import lm
from database import  db_session
from sqlalchemy.exc import IntegrityError
from DoctorSpring.models import User,Patient,Doctor,Diagnose ,DiagnoseTemplate
from DoctorSpring.models import User,Comment,Message ,UserFavorites,UserRole ,TanksNote
from DoctorSpring.util import result_status as rs,object2dict,pdf_utils,constant,authenticated
from DoctorSpring.util.constant import MessageUserType,Pagger,ReportType,ReportStatus
from param_service import UserCenter
from database import db_session
from datetime import datetime

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


@uc.route('/admin/diagnose/list/all',  methods = ['GET', 'POST'])
@authenticated('admin',constant.RoleId.Admin)
def getDiagnoseListByAdmin2():

    userId=session['userId']
    # user=User.getById(userId)
    # if user is None:
    #     return  json.dumps(rs.NO_DATA.__dict__,ensure_ascii=False)
    #     #权限查看
    # if UserRole.checkRole(db_session,userId,constant.RoleId.Admin):
    #     return  json.dumps(rs.PERMISSION_DENY.__dict__,ensure_ascii=False)

    hostpitalIds=request.args.get('hostpitalId')
    hostpitalList=UserCenter.getDiagnoseListByAdmin(hostpitalIds)
    doctorName=request.args.get('doctorName')
    pageNo=request.args.get('pageNo')
    pageSize=request.args.get('pageSize')
    pager=Pagger(pageNo,pageSize)
    diagnoses=Diagnose.getDiagnoseByAdmin2(db_session,hostpitalList,doctorName,pager)
    diagnosesDict=dataChangeService.userCenterDiagnoses(diagnoses)


    resultStatus=rs.ResultStatus(rs.SUCCESS.status,rs.SUCCESS.msg,diagnosesDict)
    resultDict=resultStatus.__dict__
    return json.dumps(resultDict,ensure_ascii=False)

@uc.route('/admin/diagnose/list/my',  methods = ['GET', 'POST'])
@authenticated('admin',constant.RoleId.Admin)
def getDiagnoseListByAdmin():
    userId=session['userId']
    # user=User.getById(userId)
    # if user is None:
    #     return  json.dumps(rs.NO_DATA.__dict__,ensure_ascii=False)
    #     #权限查看
    # if UserRole.checkRole(db_session,userId,constant.RoleId.Admin):
    #     return  json.dumps(rs.PERMISSION_DENY.__dict__,ensure_ascii=False)

    status=request.args.get('status')
    startDate=datetime.strptime(request.args.get('startDate'),"%Y-%m-%d")
    endDate=datetime.strptime(request.args.get('startDate'),"%Y-%m-%d")
    pageNo=request.args.get('pageNo')
    pageSize=request.args.get('pageSize')
    pager=Pagger(pageNo,pageSize)
    diagnoses=Diagnose.getDiagnosesByAdmin(db_session,pager,status,startDate,endDate)
    diagnosesDict=dataChangeService.userCenterDiagnoses(diagnoses)
    resultStatus=rs.ResultStatus(rs.SUCCESS.status,rs.SUCCESS.msg,diagnosesDict)
    resultDict=resultStatus.__dict__
    return json.dumps(resultDict,ensure_ascii=False)

@uc.route('/admin/diagnose/list/my',  methods = ['GET', 'POST'])
@authenticated('admin',constant.RoleId.Doctor)
def getDiagnoseListByDoctor():
    userId=session['userId']
    # user=User.getById(userId)
    # if user is None:
    #     return  json.dumps(rs.NO_DATA.__dict__,ensure_ascii=False)
    #     #权限查看
    # if UserRole.checkRole(db_session,userId,constant.RoleId.Admin):
    #     return  json.dumps(rs.PERMISSION_DENY.__dict__,ensure_ascii=False)
    doctor=Doctor.getByUserId(userId)
    if doctor:

        status=request.args.get('status')
        startDate=datetime.strptime(request.args.get('startDate'),"%Y-%m-%d")
        endDate=datetime.strptime(request.args.get('startDate'),"%Y-%m-%d")
        pageNo=request.args.get('pageNo')
        pageSize=request.args.get('pageSize')
        pager=Pagger(pageNo,pageSize)
        diagnoses=Diagnose.getDiagnosesByDoctorId(db_session,pager,status,startDate,endDate)
        diagnosesDict=dataChangeService.userCenterDiagnoses(diagnoses)
        resultStatus=rs.ResultStatus(rs.SUCCESS.status,rs.SUCCESS.msg,diagnosesDict)
        resultDict=resultStatus.__dict__
        return json.dumps(resultDict,ensure_ascii=False)
    return json.dumps(rs.FAILURE.__dict__,ensure_ascii=False)
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



@uc.route('/userFavorties/add',  methods = ['GET', 'POST'])
def addUserFavorties():
    form =  UserFavortiesForm(request.args)
    formResult=form.validate()

    userId=session['userId']
    if userId is None:
        return json.dumps(rs.NO_LOGIN.__dict__,ensure_ascii=False)

    if formResult.status==rs.SUCCESS.status:
        #session['remember_me'] = form.remember_me.data
        # login and validate the user...
        userFavorites=UserFavorites(userId,form.type,form.doctorId,form.hospitalId,form.docId)
        UserFavorites.save(userFavorites)
        #flash('成功添加诊断评论')
        return json.dumps(formResult.__dict__,ensure_ascii=False)
    return json.dumps(formResult.__dict__,ensure_ascii=False)
@uc.route('/userFavorties/<int:id>/cancel',  methods = ['GET', 'POST'])
def cancleUserFavorties(id):
    UserFavorites.cancleFavorites(id)
    return json.dumps(rs.SUCCESS.__dict__,ensure_ascii=False)
@uc.route('/userFavorties/<int:userId>/list',  methods = ['GET', 'POST'])
def getUserFavorties(userId):
    type=request.args.get('type')
    userFavorites=UserFavorites.getUserFavorties(userId,type)
    userFavoritesDict=object2dict.objects2dicts(userFavorites)
    resultStatus=rs.ResultStatus(rs.SUCCESS.status,rs.SUCCESS.msg,userFavoritesDict)
    return json.dumps(resultStatus.__dict__,ensure_ascii=False)

@uc.route('/diagnose/<int:diagnoseId>/pdf', methods=['GET','POST'])
def generatorPdf(diagnoseId):
    diagnose=Diagnose.getDiagnoseById(diagnoseId)
    report=None
    if hasattr(diagnose,'report'):
        report=diagnose.report
        if diagnose and report and report.status==ReportStatus.Commited and report.type==ReportType.Doctor:
            data={}
            data['techDesc']=report.techDesc
            data['imageDesc']=report.imageDesc
            data['diagnoseDesc']=report.diagnoseDesc
            data['seriesNumber']=report.seriesNumber
            data['fileUrl']=report.fileUrl
            createDate=report.createDate
            if createDate:
                createDate=createDate.strftime('%Y-%m-%d')
                data['createDate']=createDate

            postions=dataChangeService.getDiagnosePositonFromDiagnose(diagnose)
            if postions:
                data['postions']=postions
            if hasattr(diagnose,'patient'):
                data['gender']=diagnose.patient.gender
                birthDate=diagnose.patient.birthDate
                if birthDate:
                    birthDate=birthDate.strftime('%Y-%m-%d')
                    data['birthDate']=birthDate
                data['name']=diagnose.patient.name
            if hasattr(diagnose,'doctor'):
                data['doctorName']=diagnose.doctor.username

            html =  render_template('diagnoseResultPdf.html',data=data)
            result = open(constant.DirConstant.DIAGNOSE_PDF_DIR+'test.pdf', 'wb') # Changed from file to filename
            pdf = pdf_utils.save_pdf(html,result)
            result.close()
            # return render_template("testpdf.html",getAvatar=getAvatar)
            return html
    return None



@uc.route('/gratitude/create',  methods = ['GET', 'POST'])
def addThankNote():
    form =  ThanksNoteForm(request.form)
    formResult=form.validate()
    userId=session['userId']
    if userId is None:
        json.dumps(rs.NO_LOGIN.__dict__,ensure_ascii=False)
    if formResult.status==rs.SUCCESS.status:
        thanksNote=TanksNote(userId,form.receiver,form.title,form.content)
        TanksNote.save(db_session,thanksNote)
        return json.dumps(formResult.__dict__,ensure_ascii=False)
    return json.dumps(formResult.__dict__,ensure_ascii=False)



@uc.route('/gratitude/<int:userid>/list', methods = ['GET', 'POST'])
def getThanksNotes(userid):
    status=request.args.get('status')

    pageNo=request.args.get('pageNo')
    pageSize=request.args.get('pageSize')
    pager=Pagger(pageNo,pageSize)

    thanksNotes=TanksNote.getThanksNoteByReceiver(db_session,userid)
    if thanksNotes is None or len(thanksNotes)<1:
        return jsonify(rs.SUCCESS.__dict__)
    thanksNotesDict=object2dict.objects2dicts(thanksNotes)
    dataChangeService.setThanksNoteDetail(thanksNotesDict)
    resultStatus=rs.ResultStatus(rs.SUCCESS.status,rs.SUCCESS.msg,thanksNotesDict)
    resultDict=resultStatus.__dict__
    return jsonify(resultDict)
@uc.route('/redirectPdf', methods=['GET','POST'])
def testRedirect():
    #return redirect("/pdf")
    print url_for('user_center.generatorPdf',diagnoseName='ccheng')
    return redirect(url_for('user_center.generatorPdf'))




