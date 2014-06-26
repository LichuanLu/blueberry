# coding: utf-8
__author__ = 'ccheng'

from flask import Flask, request, session, g, redirect, url_for, Blueprint, jsonify
from flask import abort, render_template, flash
from flask.ext.login import login_user, logout_user, current_user, login_required
from forms import LoginForm ,CommentsForm ,ReportForm
from DoctorSpring import lm
from database import  db_session
from sqlalchemy.exc import IntegrityError
from DoctorSpring.models import User,Patient,Doctor,Diagnose ,DiagnoseTemplate,Report,UserRole
from DoctorSpring.models import User,Comment,Message,DiagnoseLog
from DoctorSpring.util import result_status as rs,object2dict ,constant,pdf_utils
from DoctorSpring.util.authenticated import authenticated
from DoctorSpring.util.constant import MessageUserType,Pagger
import string



import  data_change_service as dataChangeService
import json

import config
config = config.rec()

diagnoseView = Blueprint('diagnose', __name__)



#领取诊断
@diagnoseView.route('/admin/diagnose/update',  methods = ['GET', 'POST'])
@authenticated('admin',constant.RoleId.Admin)
def fetchDiagnoseByAdmin():

    diagnoseId=request.form.get('diagnoseId')
    userId=session['userId']


    # if diagnoseId is None :
    #     return  json.dumps(rs.PARAM_ERROR.__dict__,ensure_ascii=False)
    #
    # user=User.getById(userId)
    # if user is None:
    #     return  json.dumps(rs.NO_DATA.__dict__,ensure_ascii=False)
    #
    # from database import db_session
    # if UserRole.checkRole(db_session,userId,constant.RoleId.Admin):
    #     result=Diagnose.addAdminIdAndChangeStatus(diagnoseId,userId)
    #     #诊断日志
    #     diagoseLog=DiagnoseLog(userId,diagnoseId,constant.DiagnoseLogAction.FetchDiagnoseAction)
    #     DiagnoseLog.save(db_session,diagoseLog)
    #
    #     return json.dumps(rs.SUCCESS.__dict__,ensure_ascii=False)
    # else:
    #     return json.dumps(rs.PERMISSION_DENY.__dict__,ensure_ascii=False)



    result=Diagnose.addAdminIdAndChangeStatus(diagnoseId,userId)
    #诊断日志
    if result:
        diagoseLog=DiagnoseLog(userId,diagnoseId,constant.DiagnoseLogAction.FetchDiagnoseAction)
        DiagnoseLog.save(db_session,diagoseLog)

        return json.dumps(rs.SUCCESS.__dict__,ensure_ascii=False)
    return json.dumps(rs.FAILURE.__dict__,ensure_ascii=False)

#初诊断
@diagnoseView.route('/admin/report/addOrUpate',  methods = ['GET', 'POST'])
def addOrUpdateReport():

    userId=session['userId']
    user=User.getById(userId)


    if user is None  :
        return  json.dumps(rs.NO_DATA.__dict__,ensure_ascii=False)
    #权限查看
    if  UserRole.checkRole(db_session,userId,constant.RoleId.Admin) == False:
        return  json.dumps(rs.PERMISSION_DENY.__dict__,ensure_ascii=False)

    form =  ReportForm(request.form)
    formResult=form.validate()
    if formResult.status==rs.SUCCESS.status:
        diagnose=Diagnose.getDiagnoseById(form.diagnoseId)
        if diagnose is None:
            return  json.dumps(rs.NO_DATA.__dict__,ensure_ascii=False)
        #session['remember_me'] = form.remember_me.data
        # login and validate the user...
        if form.reportId:
            report=Report.getReportById(form.reportId)
            if report.type==constant.ReportType.Doctor:
                return  json.dumps(rs.PERMISSION_DENY.__dict__,ensure_ascii=False)
            Report.update(form.reportId,None,form.status,None,form.techDesc,form.imageDesc,form.diagnoseDesc)
        else:
            report=Report(form.techDesc,form.imageDesc,form.diagnoseDesc,form.fileUrl,form.status)
            Report.save(report)

            diagnose.reportId=report.id
            Diagnose.save(diagnose)
        #flash('成功添加诊断评论')
        if form.status and form.status == constant.ReportStatus.Commited:
            diagnose=Diagnose.getDiagnoseById(form.diagnoseId)
            if diagnose:
                Diagnose.changeDiagnoseStatus(diagnose.id,constant.DiagnoseStatus.NeedDiagnose)
            Report.update(form.reportId,constant.ReportType.Doctor,status=constant.ReportStatus.Draft)
            if diagnose and hasattr(diagnose,'doctor'):
                doctor=diagnose.doctor
                if doctor and doctor.userId:
                    content=dataChangeService.getDoctorNeedDiagnoseMessageContent(diagnose,doctor)

                    #诊断通知
                    message=Message(constant.DefaultSystemAdminUserId,doctor.userId,'诊断通知',content,constant.MessageType.Diagnose)
                    Message.save(message)

                    #诊断日志
                    diagoseLog=DiagnoseLog(userId,form.diagnoseId,constant.DiagnoseLogAction.FetchDiagnoseAction)
                    DiagnoseLog.save(db_session,diagoseLog)

            return json.dumps(formResult.__dict__,ensure_ascii=False)
    return json.dumps(formResult.__dict__,ensure_ascii=False)
#诊断
@diagnoseView.route('/doctor/report/update',  methods = ['GET', 'POST'])
def updateReport():

    userId=session['userId']
    user=User.getById(userId)
    if user is None:
        return  json.dumps(rs.NO_DATA.__dict__,ensure_ascii=False)

    # if UserRole.checkRole(db_session,userId,constant.RoleId.Doctor):
    #     return  json.dumps(rs.PERMISSION_DENY.__dict__,ensure_ascii=False)

    form =  ReportForm(request.form)

    if form.reportId:
        #session['remember_me'] = form.remember_me.data
        # login and validate the user...
        if form.status and form.status==constant.ReportStatus.Commited:

            fileUrl=pdf_utils.generatorPdf(form.diagnoseId)#需要先生存文檔上傳到服務器，獲取url
            report=Report.update(form.reportId,constant.ReportType.Doctor,form.status,fileUrl,form.techDesc,form.imageDesc,form.diagnoseDesc)
            Diagnose.changeDiagnoseStatus(form.diagnoseId,constant.DiagnoseStatus.Diagnosed)
            #需要給用戶發信和記錄操作日誌
            diagnose=Diagnose.getDiagnoseById(form.diagnoseId)
            sendMessageAndRecordLog(diagnose,userId)

        else:
            fileUrl=None#這是草稿，不需要生存文檔

            diagnose=Diagnose.getDiagnoseById(form.diagnoseId)
            if diagnose is None:
                return  json.dumps(rs.NO_DATA.__dict__,ensure_ascii=False)
            report=Report.update(form.reportId,constant.ReportType.Doctor,form.status,fileUrl,form.techDesc,form.imageDesc,form.diagnoseDesc)
            recordDiagnoseLog(diagnose,userId)

        return json.dumps(rs.SUCCESS.__dict__,ensure_ascii=False)
    return json.dumps(rs.FAILURE.__dict__,ensure_ascii=False)
def sendMessageAndRecordLog(diagnose,userId):
    if diagnose and hasattr(diagnose,'patient') and diagnose.patient.userID:
        userId=diagnose.patient.userID
        content=dataChangeService.getPatienDiagnoseMessageContent(diagnose)
        message=Message(constant.DefaultSystemAdminUserId,diagnose.patient.userID,'诊断通知',content,constant.MessageType.Diagnose)
        Message.save(message)

    diagnoseLog=DiagnoseLog(userId,diagnose.id,constant.DiagnoseLogAction.DiagnoseFinished)
    DiagnoseLog.save(db_session,diagnoseLog)

def recordDiagnoseLog(diagnose,userId):
    diagnoseLog=DiagnoseLog(userId,diagnose.id,constant.DiagnoseLogAction.UpateDiagnoseAction)
    DiagnoseLog.save(db_session,diagnoseLog)



@diagnoseView.route('/report/<int:reportId>',  methods = ['GET', 'POST'])
def getReport(reportId):
     report=Report.getReportById(reportId)
     if report:
         reportDict=object2dict.to_json(report,report.__class__)
         resultStatus=rs.ResultStatus(rs.SUCCESS.status,rs.SUCCESS.msg,reportDict)
         resultDict=resultStatus.__dict__
         return json.dumps(resultDict,ensure_ascii=False)
     return json.dumps(rs.NO_DATA,ensure_ascii=False)

@diagnoseView.route('/diagnose/reportdetail',  methods = ['GET', 'POST'])
def getDiagnoseDetailInfo():
    diagnoseId=request.args.get('diagnoseId')
    if diagnoseId:
        diagnoseId=string.atoi(diagnoseId)
    else:
        return json.dumps(rs.PARAM_ERROR,ensure_ascii=False)

    diagnose=Diagnose.getDiagnoseById(diagnoseId)
    if diagnose:
        diagnoseResult=dataChangeService.getDiagnoseDetailInfo(diagnose)
        resultStatus=rs.ResultStatus(rs.SUCCESS.status,rs.SUCCESS.msg,diagnoseResult)
        resultDict=resultStatus.__dict__
        return json.dumps(resultDict,ensure_ascii=False)
    return json.dumps(rs.NO_DATA,ensure_ascii=False)
@diagnoseView.route('/diagnose/actions',  methods = ['GET', 'POST'])
def getDiagnoseActions():
    try:
        diagnoseId=request.args.get('diagnoseId')

        userId=session['userId']
        if userId is None:
            return json.dumps(rs.NO_LOGIN.__dict__,ensure_ascii=False)
        userId=string.atoi(userId)

        diagnose=Diagnose.getDiagnoseById(diagnoseId)
        if diagnose is None :
            return json.dumps(rs.NO_DATA.__dict__,ensure_ascii=False)
        if hasattr(diagnose,'patient') and diagnose.patient and diagnose.patient.userID:
            if userId!=diagnose.patient.userID:
                return json.dumps(rs.PERMISSION_DENY.__dict__,ensure_ascii=False)
            diagDict=dataChangeService.getDiagnoseDetailInfoByPatient(db_session,diagnose)
        resultStatus=rs.ResultStatus(rs.SUCCESS.status,rs.SUCCESS.msg,diagDict)
        resultDict=resultStatus.__dict__
        return json.dumps(resultDict,ensure_ascii=False)


    except Exception, e:
        print e.message
        print e
        resultDict=rs.SUCCESS.__dict__
        json.dumps(resultDict,ensure_ascii=False)


@diagnoseView.route('/diagnose/delete/<int:diagnoseId>',  methods = ['GET', 'POST'])
def cancleDiagnose(diagnoseId):
    userId=session['uesrId']
    if userId is None:
        return json.dumps(rs.NO_LOGIN.__dict__,ensure_ascii=False)
    userId=string.atoi(userId)
    diagnose=Diagnose.getDiagnoseById(diagnoseId)
    if diagnose is None:
        return  json.dumps(rs.NO_DATA.__dict__,ensure_ascii=False)
    if hasattr(diagnose,'patient') and diagnose.patient and diagnose.patient.userID and  diagnose.patient.userID==userId:
         diagnose.status=constant.DiagnoseStatus.Del
         Diagnose.save(diagnose)

         diagoseLog=DiagnoseLog(userId,diagnoseId,constant.DiagnoseLogAction.CancleDiagnose)
         DiagnoseLog.save(db_session,diagoseLog)
         return  json.dumps(rs.SUCCESS.__dict__,ensure_ascii=False)
    else:
         return  json.dumps(rs.PERMISSION_DENY.__dict__,ensure_ascii=False)

@diagnoseView.route('/diagnose/rollback/<int:diagnoseId>',  methods = ['GET', 'POST'])
def rollbackDiagnose(diagnoseId):
    userId=session['uesrId']
    if userId is None:
        return json.dumps(rs.NO_LOGIN.__dict__,ensure_ascii=False)
    userId=string.atoi(userId)

    status=request.args.get('status')
    comments=request.args.get('comments')
    if status:
        status=string.atoi(status)
    diagnose=Diagnose.getDiagnoseById(diagnoseId)
    if diagnose is None:
        return  json.dumps(rs.NO_DATA.__dict__,ensure_ascii=False)
    if hasattr(diagnose,'uploadUser') and diagnose.uploadUserId and  diagnose.uploadUserId==userId:
        if status is None:
            status=constant.DiagnoseStatus.Draft
        diagnose.status=status
        Diagnose.save(diagnose)

        diagoseLog=DiagnoseLog(userId,diagnoseId,constant.DiagnoseLogAction.DiagnoseNeedUpateAction)
        diagoseLog.description=comments
        DiagnoseLog.save(db_session,diagoseLog)

        if hasattr(diagnose,'patient') and diagnose.patient.userID:
            content=dataChangeService.getPatienDiagnoseMessageContent(diagnose)

            #诊断通知
            message=Message(constant.DefaultSystemAdminUserId,diagnose.patient.userID,'诊断通知',content,constant.MessageType.Diagnose)
            Message.save(message)

        return  json.dumps(rs.SUCCESS.__dict__,ensure_ascii=False)
    else:
        return  json.dumps(rs.PERMISSION_DENY.__dict__,ensure_ascii=False)


@diagnoseView.route('/diagnose/evaluate/<int:diagnoseId>',  methods = ['GET', 'POST'])
def evaluateDiagnose(diagnoseId):
    userId=session['uesrId']
    if userId is None:
        return json.dumps(rs.NO_LOGIN.__dict__,ensure_ascii=False)
    userId=string.atoi(userId)

    score=request.args.get('score')
    description=request.args.get('description')
    if score:
        score=string.atoi(score)
    else:
        return  json.dumps(rs.PARAM_ERROR.__dict__,ensure_ascii=False)

    diagnose=Diagnose.getDiagnoseById(diagnoseId)
    if diagnose is None:
        return  json.dumps(rs.NO_DATA.__dict__,ensure_ascii=False)
    if hasattr(diagnose,'patient') and diagnose.patient and diagnose.patient.userID and  diagnose.patient.userID==userId:
        diagnose.status=constant.DiagnoseStatus.Diagnosed
        diagnose.score=score
        Diagnose.save(diagnose)

        diagoseLog=DiagnoseLog(userId,diagnoseId,constant.DiagnoseLogAction.DiagnoseFinished)
        diagoseLog.description=description
        DiagnoseLog.save(db_session,diagoseLog)
        return  json.dumps(rs.SUCCESS.__dict__,ensure_ascii=False)
    else:
        return  json.dumps(rs.PERMISSION_DENY.__dict__,ensure_ascii=False)


