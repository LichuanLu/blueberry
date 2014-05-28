# coding: utf-8
__author__ = 'ccheng'

from flask import Flask, request, session, g, redirect, url_for, Blueprint, jsonify
from flask import abort, render_template, flash
from flask.ext.login import login_user, logout_user, current_user, login_required
from forms import LoginForm, RegisterForm ,CommentsForm ,MessageForm,ReportForm
from DoctorSpring import lm
from database import  db_session
from sqlalchemy.exc import IntegrityError
from DoctorSpring.models import User,Patient,Doctor,Diagnose ,DiagnoseTemplate,Report
from DoctorSpring.models import User,Comment,Message
from DoctorSpring.util import result_status as rs,object2dict ,constant
from DoctorSpring.util.constant import MessageUserType,Pagger


import  data_change_service as dataChangeService
import json

import config
config = config.rec()

diagnoseView = Blueprint('diagnose', __name__)


@diagnoseView.route('/admin/report/addOrUpate',  methods = ['GET', 'POST'])
def addOrUpdateReport():
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
        if form.status and constant.ReportStatus.Commited:
            diagnose=Diagnose.getDiagnoseById(form.diagnoseId)
            if diagnose:
                Diagnose.changeDiagnoseStatus(diagnose.id,constant.DiagnoseStatus.NeedDiagnose)
            if diagnose and hasattr(diagnose,'doctor'):
                doctor=diagnose.doctor
                if doctor and doctor.userId:
                    content=dataChangeService.getDoctorNeedDiagnoseMessageContent(diagnose,doctor)
                    message=Message(constant.DefaultSystemAdminUserId,doctor.userId,'诊断通知',content,constant.MessageType.Diagnose)
                    Message.save(message)
            return json.dumps(formResult.__dict__,ensure_ascii=False)
    return json.dumps(formResult.__dict__,ensure_ascii=False)
@diagnoseView.route('/doctor/report/update',  methods = ['GET', 'POST'])
def updateReport():
    form =  ReportForm(request.form)

    if form.reportId:
        #session['remember_me'] = form.remember_me.data
        # login and validate the user...
        if form.status and form.status==constant.ReportStatus.Commited:
            fileUrl=None#需要先生存文檔上傳到服務器，獲取url
            report=Report.update(form.reportId,constant.ReportType.Doctor,form.status,fileUrl,form.techDesc,form.imageDesc,form.diagnoseDesc)
            Diagnose.changeDiagnoseStatus(form.diagnoseId,constant.DiagnoseStatus.Diagnosed)
            #需要給用戶發信和記錄操作日誌
        else:
            fileUrl=None#這是草稿，不需要生存文檔
            report=Report.update(form.reportId,constant.ReportType.Doctor,form.status,fileUrl,form.techDesc,form.imageDesc,form.diagnoseDesc)

        return json.dumps(rs.SUCCESS.__dict__,ensure_ascii=False)
    return json.dumps(rs.FAILURE.__dict__,ensure_ascii=False)

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


