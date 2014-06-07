# coding: utf-8
__author__ = 'ccheng'

from flask import Flask, request, session, g, redirect, url_for, Blueprint, jsonify
from flask import abort, render_template, flash
from flask.ext.login import login_user, logout_user, current_user, login_required
from forms import LoginForm, RegisterForm ,CommentsForm ,MessageForm,ReportForm
from DoctorSpring import lm
from database import  db_session
from sqlalchemy.exc import IntegrityError
from DoctorSpring.models import User,Patient,Doctor,Diagnose ,DiagnoseTemplate,Report,UserRole
from DoctorSpring.models import User,Comment,Message,DiagnoseLog
from DoctorSpring.util import result_status as rs,object2dict ,constant
from DoctorSpring.util.authenticated import authenticated
from DoctorSpring.util.constant import MessageUserType,Pagger



import  data_change_service as dataChangeService
import json

import config
config = config.rec()

diagnoseView = Blueprint('diagnose', __name__)



#领取诊断
@diagnoseView.route('/admin/diagnose/update',  methods = ['GET', 'POST'])
@authenticated('admin',constant.RoleId.Admin)
def fetchDiagnoseByAdmin():

    diagnoseId=request.args.get('diagnoseId')
    userId=4#session['userId']


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

    userId=5#session['userId']
    user=User.getById(userId)
    if user is None:
        return  json.dumps(rs.NO_DATA.__dict__,ensure_ascii=False)
    #权限查看
    if  UserRole.checkRole(db_session,userId,constant.RoleId.Admin) == False:
        return  json.dumps(rs.PERMISSION_DENY.__dict__,ensure_ascii=False)

    form =  ReportForm(request.form)
    formResult=form.validate()
    if formResult.status==rs.SUCCESS.status:
        #session['remember_me'] = form.remember_me.data
        # login and validate the user...
        if form.reportId:
            Report.update(form.reportId,None,form.status,None,form.techDesc,form.imageDesc,form.diagnoseDesc)
        else:
            report=Report(form.techDesc,form.imageDesc,form.diagnoseDesc,form.fileUrl,form.status)
            Report.save(report)
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

    userId=4#session['userId']
    user=User.getById(userId)
    if user is None:
        return  json.dumps(rs.NO_DATA.__dict__,ensure_ascii=False)

    if UserRole.checkRole(db_session,userId,constant.RoleId.Doctor):
        return  json.dumps(rs.PERMISSION_DENY.__dict__,ensure_ascii=False)

    form =  ReportForm(request.form)

    if form.reportId:
        #session['remember_me'] = form.remember_me.data
        # login and validate the user...
        if form.status and form.status==constant.ReportStatus.Commited:
            fileUrl=None#需要先生存文檔上傳到服務器，獲取url
            report=Report.update(form.reportId,constant.ReportType.Doctor,form.status,fileUrl,form.techDesc,form.imageDesc,form.diagnoseDesc)
            Diagnose.changeDiagnoseStatus(form.diagnoseId,constant.DiagnoseStatus.Diagnosed)
            #需要給用戶發信和記錄操作日誌
            diagnose=Diagnose.getDiagnoseById(form.diagnoseId)
            sendMessageAndRecordLog(diagnose)

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
    DiagnoseLog.save(diagnoseLog)

def recordDiagnoseLog(diagnose,userId):
    diagnoseLog=DiagnoseLog(userId,diagnose.id,constant.DiagnoseLogAction.UpateDiagnoseAction)
    DiagnoseLog.save(diagnoseLog)



@diagnoseView.route('/report/<int:reportId>',  methods = ['GET', 'POST'])
def getReport(reportId):
     report=Report.getReportById(reportId)
     if report:
         reportDict=object2dict.to_json(report,report.__class__)
         resultStatus=rs.ResultStatus(rs.SUCCESS.status,rs.SUCCESS.msg,reportDict)
         resultDict=resultStatus.__dict__
         return json.dumps(resultDict,ensure_ascii=False)
     return json.dumps(rs.NO_DATA,ensure_ascii=False)

@diagnoseView.route('/diagnose/<int:diagnoseId>/detailInfo',  methods = ['GET', 'POST'])
def getDiagnoseDetailInfo(diagnoseId):
    diagnose=Diagnose.getDiagnoseById(diagnoseId)
    if diagnose:
        diagnoseResult=dataChangeService.getDiagnoseDetailInfo(diagnose)
        resultStatus=rs.ResultStatus(rs.SUCCESS.status,rs.SUCCESS.msg,diagnoseResult)
        resultDict=resultStatus.__dict__
        return json.dumps(resultDict,ensure_ascii=False)
    return json.dumps(rs.NO_DATA,ensure_ascii=False)
@diagnoseView.route('/admin/getDiagnose',  methods = ['GET', 'POST'])
def getDiagnose():
    try:
        diagnoseId=request.args.get('diagnoseId')
        adminId=request.args.get('userId')
        Diagnose.addAdminIdAndChangeStatus(diagnoseId,adminId)
        resultDict=rs.SUCCESS.__dict__
        json.dumps(resultDict,ensure_ascii=False)
    except Exception, e:
        print e.message
        print e
        resultDict=rs.SUCCESS.__dict__
        json.dumps(resultDict,ensure_ascii=False)




