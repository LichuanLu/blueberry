# coding: utf-8
__author__ = 'ccheng'

from flask import Flask, request, session, g, redirect, url_for, Blueprint, jsonify
from flask import abort, render_template, flash
from flask.ext.login import login_user, logout_user, current_user, login_required
from forms import LoginForm, RegisterForm ,CommentsForm ,MessageForm,ReportForm
from DoctorSpring import lm
from database import  db_session
from sqlalchemy.exc import IntegrityError
from DoctorSpring.models import User,Patent,Doctor,Diagnose ,DiagnoseTemplate,Report
from DoctorSpring.models import User,Comment,Message
from DoctorSpring.util import result_status as rs,object2dict
from DoctorSpring.util.constant import MessageUserType,Pagger

import  data_change_service as dataChangeService
import json

import config
config = config.rec()

diagnoseView = Blueprint('diagnose', __name__)


@diagnoseView.route('/doctor/report/add',  methods = ['GET', 'POST'])
def addReport():
    form =  ReportForm(request.form)
    formResult=form.validate()
    if formResult.status==rs.SUCCESS.status:
        #session['remember_me'] = form.remember_me.data
        # login and validate the user...
        report=Report(form.techDesc,form.imageDesc,form.diagnoseDesc,form.fileUrl,form.status)
        Report.save(report)
        #flash('成功添加诊断评论')
        return json.dumps(formResult.__dict__,ensure_ascii=False)
    return json.dumps(formResult.__dict__,ensure_ascii=False)
@diagnoseView.route('/doctor/report/update',  methods = ['GET', 'POST'])
def updateReport():
    form =  ReportForm(request.form)

    if form.reportId:
        #session['remember_me'] = form.remember_me.data
        # login and validate the user...
        report=Report.update(form.reportId,form.status,form.fileUrl,form.techDesc,form.imageDesc,form.diagnoseDesc)

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

