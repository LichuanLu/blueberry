# coding: utf-8
__author__ = 'ccheng'

from flask import Flask, request, session, g, redirect, url_for, Blueprint, jsonify
from flask import abort, render_template, flash
from flask.ext.login import login_user, logout_user, current_user, login_required
from forms import LoginForm ,CommentsForm ,UserFavortiesForm,ThanksNoteForm
from DoctorSpring import lm
from database import  db_session
from sqlalchemy.exc import IntegrityError
from DoctorSpring.models import User,Patient,Doctor,Diagnose ,DiagnoseTemplate,DoctorProfile
from DoctorSpring.models import User,Comment,Message ,UserFavorites,UserRole ,ThanksNote
from DoctorSpring.util import result_status as rs,object2dict,pdf_utils,constant
from DoctorSpring.util.constant import MessageUserType,Pagger,ReportType,ReportStatus
from DoctorSpring.util.authenticated import authenticated
from param_service import UserCenter
from database import db_session
from datetime import datetime
import string

import  data_change_service as dataChangeService
import json

import config
config = config.rec()

uc = Blueprint('user_center', __name__)


@uc.route('/doctorhome',  methods = ['GET', 'POST'])
def endterDoctorHome():
    userId=session['userId']
    doctor=Doctor.getByUserId(userId)

    if doctor is None:
        return redirect(url_for('/300'))

    resultDate={}
    messageCount=Message.getMessageCountByReceiver(userId)
    resultDate['messageCount']=messageCount

    diagnoseCount=Diagnose.getNewDiagnoseCountByDoctorId(doctor.id)
    resultDate['diagnoseCount']=diagnoseCount

    resultDate['doctor']=doctor
    pager=Pagger(1,20)
    diagnoses=Diagnose.getDiagnosesByDoctorId(db_session,doctor.id,pager)
    diagnoseDict=dataChangeService.userCenterDiagnoses(diagnoses)
    resultDate['diagnoses']=diagnoseDict
    return render_template("doctorHome.html",data=resultDate)

@uc.route('/patienthome',  methods = ['GET', 'POST'])
def endterPatientHome():
    userId=session['userId']
    user=User.getById(userId)

    if user is None:
        return redirect(url_for('/300'))

    resultDate={}
    messageCount=Message.getMessageCountByReceiver(userId)
    resultDate['messageCount']=messageCount

    diagnoseCount=Diagnose.getNewDiagnoseCountByUserId(userId)
    resultDate['diagnoseCount']=diagnoseCount

    resultDate['user']=user
    #pager=Pagger(1,20)
    # diagnoses=Diagnose.getDiagnosesByDoctorId(db_session,doctor.id,pager)
    # diagnoseDict=dataChangeService.userCenterDiagnoses(diagnoses)
    # resultDate['diagnoses']=diagnoseDict
    return render_template("patientHome.html",data=resultDate)

@uc.route('/hospital/user',  methods = ['GET', 'POST'])
def endterHospitalUserHome():
    userId=session['userId']
    user=User.getById(userId)

    if user is None:
        return redirect(url_for('/300'))

    resultDate={}
    # messageCount=Message.getMessageCountByReceiver(userId)
    # resultDate['messageCount']=messageCount
    #
    # diagnoseCount=Diagnose.getNewDiagnoseCountByUserId(userId)
    # resultDate['diagnoseCount']=diagnoseCount
    #
    # resultDate['user']=user
    #pager=Pagger(1,20)
    # diagnoses=Diagnose.getDiagnosesByDoctorId(db_session,doctor.id,pager)
    # diagnoseDict=dataChangeService.userCenterDiagnoses(diagnoses)
    # resultDate['diagnoses']=diagnoseDict
    return render_template("hospitalUser.html",data=resultDate)




@uc.route('/doctor/site/<int:userId>',  methods = ['GET', 'POST'])
def endterDoctorSite(userId):

    #user=User.getById(userId)
    doctor=Doctor.getByUserId(userId)

    if  doctor is None:
        return redirect(url_for('/300'))

    if  hasattr(doctor,'user') !=True:
        return redirect(url_for('/300'))

    resultDate={}
    userFavortiesCount=UserFavorites.getFavortiesCountByDoctorId(doctor.id)
    resultDate['userFavortiesCount']=userFavortiesCount

    diagnoseCount=Diagnose.getDiagnoseCountByDoctorId(db_session,doctor.id)
    resultDate['diagnoseCount']=diagnoseCount

    goodDiagnoseCount=Diagnose.getDiagnoseCountByDoctorId(db_session,doctor.id,1)#good
    goodDiagnoseCount+=Diagnose.getDiagnoseCountByDoctorId(db_session,doctor.id,2)
    resultDate['goodDiagnoseCount']=goodDiagnoseCount

    resultDate['doctor']=dataChangeService.get_doctor(doctor)

    thanksNoteCount=ThanksNote.getThanksNoteCountByReceiver(db_session,userId)
    resultDate['thanksNoteCount']=thanksNoteCount

    diagnoseCommentCount=Comment.getCountByReceiver(userId)
    resultDate['diagnoseCommentCount']=diagnoseCommentCount

    if session.has_key('userId'):
        loginUserId=session.get('userId')
        if loginUserId:
            loginUserId=string.atoi(loginUserId)
            userfavor=UserFavorites.getUerFavortiesByNormalStatus(db_session,loginUserId,constant.UserFavoritesType.Doctor,doctor.id)
            if userfavor:
                resultDate['userFavortiesId']=userfavor.id





    pager=constant.Pagger(1,10)

    diagnoseComments=Comment.getCommentByReceiver(userId,constant.ModelStatus.Normal,constant.CommentType.DiagnoseComment,pager)
    if diagnoseComments  and  len(diagnoseComments)>0:
        diagnoseCommentsDict=object2dict.objects2dicts(diagnoseComments)
        dataChangeService.setDiagnoseCommentsDetailInfo(diagnoseCommentsDict)
        resultDate['comments']=diagnoseCommentsDict
    else:
        resultDate['comments']=None


    thanksNotes=ThanksNote.getThanksNoteByReceiver(db_session,userId)
    if thanksNotes  and  len(thanksNotes)>0:
        thanksNotesDict=object2dict.objects2dicts(thanksNotes)
        dataChangeService.setThanksNoteDetail(thanksNotesDict)
        resultDate['thanksNotes']=thanksNotesDict

    intros=DoctorProfile.getDoctorProfiles(userId,constant.DoctorProfileType.Intro)
    resultDate['intros']=object2dict.objects2dicts(intros)

    resumes=DoctorProfile.getDoctorProfiles(userId,constant.DoctorProfileType.Resume)
    resultDate['resumes']=object2dict.objects2dicts(resumes)

    awards=DoctorProfile.getDoctorProfiles(userId,constant.DoctorProfileType.Award)
    resultDate['awards']=object2dict.objects2dicts(awards)

    others=DoctorProfile.getDoctorProfiles(userId,constant.DoctorProfileType.Other)
    resultDate['others']=object2dict.objects2dicts(others)

    return render_template("doctorsite.html",data=resultDate)




@uc.route('/admin/diagnose/list/all',  methods = ['GET', 'POST'])
@authenticated('admin',constant.RoleId.Admin)
def getDiagnoseListByAdmin2():

    userId=session['userId']

    hostpitalIds=request.args.get('hospitalId')
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
    if status:
        import string
        status=string.atoi(status)

    startDateStr=request.args.get('startDate')
    startDate=None
    if startDateStr:
        startDate=datetime.strptime(startDateStr,"%Y-%m-%d")
    else:
        startDate=constant.SystemTimeLimiter.startTime

    endDateStr=request.args.get('endDate')
    endDate=None
    if endDateStr:
        endDate=datetime.strptime(endDateStr,"%Y-%m-%d")
    else:
        endDate=constant.SystemTimeLimiter.endTime

    pageNo=request.args.get('pageNo')
    pageSize=request.args.get('pageSize')
    pager=Pagger(pageNo,pageSize)

    diagnoses=Diagnose.getDiagnosesByAdmin(db_session,pager,status,userId,startDate,endDate)
    diagnosesDict=dataChangeService.userCenterDiagnoses(diagnoses)
    resultStatus=rs.ResultStatus(rs.SUCCESS.status,rs.SUCCESS.msg,diagnosesDict)
    resultDict=resultStatus.__dict__
    return json.dumps(resultDict,ensure_ascii=False)


@uc.route('/hospital/user/list/unfinish',  methods = ['GET', 'POST'])
#@authenticated('admin',constant.RoleId.Admin)
def getDiagnoseListByHospitalUser():

     userId=session['userId']


     pageNo=request.args.get('pageNumber')
     pageSize=request.args.get('pageSize')
     pager=Pagger(pageNo,pageSize)
     diagnoses=Diagnose.getNeedDealDiagnoseByHospitalUser(db_session,userId,None,pager)
     diagnosesDict=dataChangeService.userCenterDiagnoses(diagnoses)


     resultStatus=rs.ResultStatus(rs.SUCCESS.status,rs.SUCCESS.msg,diagnosesDict)
     resultDict=resultStatus.__dict__
     return json.dumps(resultDict,ensure_ascii=False)


@uc.route('/hospital/user/list/all',  methods = ['GET', 'POST'])
@authenticated('admin',constant.RoleId.Doctor)
def getDiagnoseListByHospitalUser2():

    userId=session['userId']

    status=request.args.get('status')
    if status:
        import string
        status=string.atoi(status)

    startDateStr=request.args.get('startDate')
    startDate=None
    if startDateStr:
        startDate=datetime.strptime(startDateStr,"%Y-%m-%d")
    else:
        startDate=constant.SystemTimeLimiter.startTime

    endDateStr=request.args.get('endDate')
    endDate=None
    if endDateStr:
        endDate=datetime.strptime(endDateStr,"%Y-%m-%d")
    else:
        endDate=constant.SystemTimeLimiter.endTime

    patientName=request.args.get('patientName')
    pageNo=request.args.get('pageNumber')
    pageSize=request.args.get('pageSize')
    pager=Pagger(pageNo,pageSize)
    diagnoses=Diagnose.getDealedDiagnoseByHospitalUser(db_session,userId,patientName,status,startDate,endDate,pager)
    diagnosesDict=dataChangeService.userCenterDiagnoses(diagnoses)


    resultStatus=rs.ResultStatus(rs.SUCCESS.status,rs.SUCCESS.msg,diagnosesDict)
    resultDict=resultStatus.__dict__
    return json.dumps(resultDict,ensure_ascii=False)


@uc.route('/diagnose/list',  methods = ['GET', 'POST'])
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

        status=request.args.get('type')
        if status:
            import string
            status=string.atoi(status)

        startDateStr=request.args.get('startDate')
        startDate=None
        if startDateStr:
            startDate=datetime.strptime(startDateStr,"%Y-%m-%d")
        else:
            startDate=constant.SystemTimeLimiter.startTime

        endDateStr=request.args.get('endDate')
        endDate=None
        if endDateStr:
            endDate=datetime.strptime(endDateStr,"%Y-%m-%d")
        else:
            endDate=constant.SystemTimeLimiter.endTime

        pageNo=request.args.get('pageNo')
        pageSize=request.args.get('pageSize')
        pager=Pagger(pageNo,pageSize)
        diagnoses=Diagnose.getDiagnosesByDoctorId(db_session,doctor.id,pager,status,startDate,endDate)
        diagnosesDict=dataChangeService.userCenterDiagnoses(diagnoses)
        resultStatus=rs.ResultStatus(rs.SUCCESS.status,rs.SUCCESS.msg,diagnosesDict)
        resultDict=resultStatus.__dict__
        return json.dumps(resultDict,ensure_ascii=False)
    return json.dumps(rs.FAILURE.__dict__,ensure_ascii=False)


@uc.route('/patient/diagnose/list',  methods = ['GET', 'POST'])
@authenticated('admin',constant.RoleId.Doctor)
def getDiagnoseListByPatient():
    userId=session['userId']
    # user=User.getById(userId)
    # if user is None:
    #     return  json.dumps(rs.NO_DATA.__dict__,ensure_ascii=False)
    #     #权限查看
    # if UserRole.checkRole(db_session,userId,constant.RoleId.Admin):
    #     return  json.dumps(rs.PERMISSION_DENY.__dict__,ensure_ascii=False)

    if userId:

        status=request.args.get('type')
        if status:
            import string
            status=string.atoi(status)

        startDateStr=request.args.get('startDate')
        startDate=None
        if startDateStr:
            startDate=datetime.strptime(startDateStr,"%Y-%m-%d")
        else:
            startDate=constant.SystemTimeLimiter.startTime

        endDateStr=request.args.get('endDate')
        endDate=None
        if endDateStr:
            endDate=datetime.strptime(endDateStr,"%Y-%m-%d")
        else:
            endDate=constant.SystemTimeLimiter.endTime

        pageNo=request.args.get('pageNo')
        pageSize=request.args.get('pageSize')
        pager=Pagger(pageNo,pageSize)
        diagnoses=Diagnose.getDiagnoseByPatientUser(db_session,userId,status,pager)
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
    if diagnosePostion:
        diagnosePostion+='\n'
    diagnoseAndImageDescs=DiagnoseTemplate.getDiagnoseAndImageDescs(diagnoseMethod,diagnosePostion)
    resultStatus=rs.ResultStatus(rs.SUCCESS.status,rs.SUCCESS.msg,diagnoseAndImageDescs)
    resultDict=resultStatus.__dict__
    return json.dumps(resultDict,ensure_ascii=False)



@uc.route('/userFavorties/add',  methods = ['GET', 'POST'])
def addUserFavorties():
    form = UserFavortiesForm(request.form)
    formResult=form.validate()

    userId=session['userId']
    if userId is None:
        return json.dumps(rs.NO_LOGIN.__dict__,ensure_ascii=False)

    if formResult.status==rs.SUCCESS.status:
        if UserFavorites.checkUerFavorties(db_session,userId,constant.UserFavoritesType.Doctor,form.doctorId):
            return json.dumps(rs.FAILURE.__dict__,ensure_ascii=False)

        userFavorites=UserFavorites.getUerFavortiesByDelStatus(db_session,userId,constant.UserFavoritesType.Doctor,form.doctorId)
        if userFavorites:
            userFavorites.status=constant.ModelStatus.Normal
            db_session.commit()
            return json.dumps(formResult.__dict__,ensure_ascii=False)
        else:
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
    if type is None:
        json.dumps(rs.PARAM_ERROR.__dict__,ensure_ascii=False)

    type=string.atoi(type)
    userFavorites=UserFavorites.getUserFavorties(userId,type)
    userFavoritesDict=dataChangeService.getUserFavoritiesDict(userFavorites)
    resultStatus=rs.ResultStatus(rs.SUCCESS.status,rs.SUCCESS.msg,userFavoritesDict)
    return json.dumps(resultStatus.__dict__,ensure_ascii=False)

@uc.route('/diagnose/<int:diagnoseId>/pdf', methods=['GET','POST'])
def generatorPdf(diagnoseId):

    diagnose=Diagnose.getDiagnoseById(diagnoseId)

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
            if hasattr(diagnose,'patient') and diagnose.patient:
                data['gender']=diagnose.patient.gender
                birthDate=diagnose.patient.birthDate
                if birthDate:
                    birthDate=birthDate.strftime('%Y-%m-%d')
                    data['birthDate']=birthDate
                data['name']=diagnose.patient.realname
            if hasattr(diagnose,'doctor'):
                data['doctorName']=diagnose.doctor.username

            html =  render_template('diagnoseResultPdf.html',data=data)
            # fileName=constant.DirConstant.DIAGNOSE_PDF_DIR+'test.pdf'
            # result = open(fileName, 'wb') # Changed from file to filename
            #
            # pdf = pdf_utils.save_pdf(html,result,diagnoseId,fileName)
            # result.close()
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

    userId=string.atoi(userId)
    if formResult.status==rs.SUCCESS.status:
        thanksNote=ThanksNote(userId,form.receiver,form.title,form.content)
        ThanksNote.save(db_session,thanksNote)
        doctor=Doctor.getByUserId(userId)
        if doctor:
            if doctor.thankNoteCount:
                doctor.thankNoteCount+=1
            else:
                doctor.thankNoteCount=1
            Doctor.save(doctor)
        return json.dumps(formResult.__dict__,ensure_ascii=False)
    return json.dumps(formResult.__dict__,ensure_ascii=False)



@uc.route('/gratitude/<int:userid>/list', methods = ['GET', 'POST'])
def getThanksNotes(userid):
    #status=request.args.get('status')

    pageNo=request.args.get('pageNo')
    pageSize=request.args.get('pageSize')
    pager=Pagger(pageNo,pageSize)

    thanksNotes=ThanksNote.getThanksNoteByReceiver(db_session,userid)
    if thanksNotes is None or len(thanksNotes)<1:
        return json.dumps(rs.SUCCESS.__dict__,ensure_ascii=False)
    thanksNotesDict=object2dict.objects2dicts(thanksNotes)
    dataChangeService.setThanksNoteDetail(thanksNotesDict)
    resultStatus=rs.ResultStatus(rs.SUCCESS.status,rs.SUCCESS.msg,thanksNotesDict)
    resultDict=resultStatus.__dict__
    return json.dumps(resultDict,ensure_ascii=False)
@uc.route('/redirectPdf', methods=['GET','POST'])
def testRedirect():
    #return redirect("/pdf")
    #print url_for('user_center.generatorPdf',diagnoseName='ccheng')
    return redirect(url_for('user_center.generatorPdf',diagnoseId=1))

@uc.route('/acount/admin', methods=['GET','POST'])
def updateAcountInfo():
    userId=None
    if session.has_key('userId'):
        userId=session['userId']
    if userId is None:
        redirect('/loginPage')

    return redirect(url_for('user_center.generatorPdf',diagnoseId=1))




