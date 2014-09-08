# coding: utf-8
__author__ = 'ccheng'

from flask import Flask, request, session, g, redirect, url_for, Blueprint, jsonify
from flask import abort, render_template, flash
from flask.ext.login import login_user, logout_user, current_user, login_required
from forms import LoginForm ,CommentsForm ,ConsultForm
from DoctorSpring import lm
from database import  db_session
from sqlalchemy.exc import IntegrityError
from DoctorSpring.models import User,Patient
from DoctorSpring.models import User,Comment,Message ,Consult,Diagnose,Doctor
from DoctorSpring.util import result_status as rs,object2dict,constant
import json
import  data_change_service as dataChangeService
from DoctorSpring import app
from config import LOGIN_URL
import config
import string
config = config.rec()
LOG=app.logger
mc = Blueprint('message_comment', __name__)


# @app.before_request
# def before_request():
#     g.user = current_user
@mc.route('/addDiagnoseComment.json', methods = ['GET', 'POST'])
def addDiagnoseComment():
    form = CommentsForm(request.form)
    resultForm=form.validate()
    if resultForm.status==rs.SUCCESS.status:
        #session['remember_me'] = form.remember_me.data
        # login and validate the user...
        diagnoseComment=Comment(form.userId,form.receiverId,form.diagnoseId,form.content)
        db_session.add(diagnoseComment)
        db_session.commit()
        db_session.flush()
        score=constant.DiagnoseScore[form.score]
        diagnose=Diagnose.getDiagnoseById(form.diagnoseId)
        diagnose.score=form.score
        Diagnose.save(diagnose)
        #为医生添加一些冗余字段
        if hasattr(diagnose,'doctor'):
            doctor=diagnose.doctor
            if score!=0:
                if doctor.goodFeedbackCount:
                    doctor.goodFeedbackCount+=1
                else:
                    doctor.goodFeedbackCount=1
            if doctor.feedbackCount:
                doctor.feedbackCount+=1
            else:
                doctor.feedbackCount=1
            Doctor.save(doctor)
        #flash('成功添加诊断评论')
        return jsonify(rs.SUCCESS.__dict__)
    return jsonify(rs.FAILURE.__dict__)
@mc.route('/observer/<int:userId>/diagnoseCommentList.json', methods = ['GET', 'POST'])
def diagnoseCommentsByObserver(userId):

    diagnoseComments=Comment.getCommentByUser(userId,type=constant.CommentType)
    if diagnoseComments is None or len(diagnoseComments)<1:
        return json.dumps(rs.SUCCESS.__dict__,ensure_ascii=False)
    diagnoseCommentsDict=object2dict.objects2dicts(diagnoseComments)
    resultStatus=rs.ResultStatus(rs.SUCCESS.status,rs.SUCCESS.msg,diagnoseCommentsDict)
    resultDict=resultStatus.__dict__
    return json.dumps(resultDict,ensure_ascii=False)
@mc.route('/receiver/<int:receiverId>/diagnoseCommentList.json', methods = ['GET', 'POST'])
def diagnoseCommentsByReceiver(receiverId):

    pageNo=request.args.get('pageNo')
    pageSize=request.args.get('pageSize')
    pager=constant.Pagger(pageNo,pageSize)

    diagnoseComments=Comment.getCommentByReceiver(receiverId,constant.ModelStatus.Normal,constant.CommentType.DiagnoseComment,pager)
    if diagnoseComments is None or len(diagnoseComments)<1:
        return jsonify(rs.SUCCESS.__dict__)

    diagnoseCommentsDict=object2dict.objects2dicts(diagnoseComments)
    dataChangeService.setDiagnoseCommentsDetailInfo(diagnoseCommentsDict)
    resultStatus=rs.ResultStatus(rs.SUCCESS.status,rs.SUCCESS.msg,diagnoseCommentsDict)
    resultDict=resultStatus.__dict__
    return jsonify(resultDict)


@mc.route('/diagnoseComment/draftList.json', methods = ['GET', 'POST'])
def diagnoseCommentsByDraft():

    pageNo=request.args.get('pageNo')
    pageSize=request.args.get('pageSize')
    pager=constant.Pagger(pageNo,pageSize)

    diagnoseComments=Comment.getCommentsByDraft(pager)
    if diagnoseComments is None or len(diagnoseComments)<1:
        return jsonify(rs.SUCCESS.__dict__)

    diagnoseCommentsDict=object2dict.objects2dicts(diagnoseComments)
    dataChangeService.setDiagnoseCommentsDetailInfo(diagnoseCommentsDict)
    resultStatus=rs.ResultStatus(rs.SUCCESS.status,rs.SUCCESS.msg,diagnoseCommentsDict)
    resultDict=resultStatus.__dict__
    return jsonify(resultDict)
@mc.route('/diagnosecomment/statuschange', methods = ['GET', 'POST'])
def changeDiagnoseCommentStatus():
    id=request.args.get('id')
    status=request.args.get('status')
    if id and status:
        result=Comment.updateComment(id,status)
        return json.dumps(rs.SUCCESS.__dict__,ensure_ascii=False)
    return json.dumps(rs.PARAM_ERROR.__dict__,ensure_ascii=False)


@mc.route('/diagnose/<int:diagnoseId>/diagnoseCommentList.json', methods = ['GET', 'POST'])
def diagnoseCommentsByDiagnose(diagnoseId):

    diagnoseComments=Comment.getCommentBydiagnose(diagnoseId)
    if diagnoseComments is None or len(diagnoseComments)<1:
        return jsonify(rs.SUCCESS.__dict__)
    diagnoseCommentsDict=object2dict.objects2dicts(diagnoseComments)
    resultStatus=rs.ResultStatus(rs.SUCCESS.status,rs.SUCCESS.msg,diagnoseCommentsDict)
    resultDict=resultStatus.__dict__
    return jsonify(resultDict)

@mc.route('/message/add', methods = ['GET', 'POST'])
def addMessage():
    form = None
    if form.validate():
        #session['remember_me'] = form.remember_me.data
        # login and validate the user...
        message=Message(form.senderId.data,form.receiverId.data,form.title.data,form.content.data,form.type.data)
        Message.save(message)
        #flash('成功添加诊断评论')
        return redirect(url_for('homepage'))
    return render_template('message.html', form=form)

@mc.route('/message/list', methods = ['GET', 'POST'])
def messagesByReceiver():
    userId=session['userId']
    status=request.args.get('status')

    messages=None
    if status:
        messages=Message.getMessageByReceiver(userId,status)
    else:
        messages=Message.getMessageByReceiver(userId)
    if messages is None or len(messages)<1:
        return jsonify(rs.SUCCESS.__dict__)
    messagesDict=object2dict.objects2dicts(messages)
    resultStatus=rs.ResultStatus(rs.SUCCESS.status,rs.SUCCESS.msg,messagesDict)
    resultDict=resultStatus.__dict__
    return jsonify(resultDict)


@mc.route('/sender/<int:senderId>/messageList.json', methods = ['GET', 'POST'])
def messagesBySender(senderId):
    status=request.args.get('status')

    messages=None
    if status:
        messages=Message.getMessageByReceiver(senderId,status)
    else:
        messages=Message.getMessageByReceiver(senderId)
    if messages is None or len(messages)<1:
        return jsonify(rs.SUCCESS.__dict__)
    messagesDict=object2dict.objects2dicts(messages)
    resultStatus=rs.ResultStatus(rs.SUCCESS.status,rs.SUCCESS.msg,messagesDict)
    resultDict=resultStatus.__dict__
    return jsonify(resultDict)

@mc.route('/message/<int:messageId>/remark.json', methods = ['GET', 'POST'])
def remarkMessage(messageId):
    status=request.args.get('status')
    result=None
    if status:
        result=Message.remarkMessage(db_session,messageId,status)
    else:
        result=Message.remarkMessage(db_session,messageId)
    resultStatus=rs.ResultStatus(rs.SUCCESS.status,rs.SUCCESS.msg,result)
    resultDict=resultStatus.__dict__
    return jsonify(resultDict)

@mc.route('/consult/add', methods = ['GET', 'POST'])
def addConsult():
    user_id=None
    if session.has_key('userId'):
        userId=session['userId']
    #userId='5'
    if userId is None:
        redirect(LOGIN_URL)
    form =  ConsultForm(request.form)
    formResult=form.validate()
    if formResult.status==rs.SUCCESS.status:
        #session['remember_me'] = form.remember_me.data
        # login and validate the user...
        consult=Consult(form.userId,form.doctorId,form.title,form.content,form.parent_id,form.source_id,form.type,form.diagnose_id)
        Consult.save(consult)
        if form.source_id:
            sourceConsult=Consult.getById(form.source_id)
            if sourceConsult:
                sourceConsult.count+=1
                Consult.update(consult)

        LOG.info(userId+' 成功添加诊断评论')
        return json.dumps(formResult.__dict__,ensure_ascii=False)
    return json.dumps(formResult.__dict__,ensure_ascii=False)


@mc.route('/doctor/<int:doctorId>/consultList', methods = ['GET', 'POST'])
def getConsultsByDoctor(doctorId):
    sourceId=request.args.get('source_id')
    if doctorId:
        consuts=None
        if sourceId:
            consuts=Consult.getConsultsByDoctorId(doctorId,string.atoi(sourceId))
        else:
            consuts=Consult.getConsultsByDoctorId(doctorId)
        consutsDict=object2dict.objects2dicts(consuts)
        dataChangeService.setConsultsResult(consutsDict)

        resultStatus=rs.ResultStatus(rs.SUCCESS.status,rs.SUCCESS.msg,consutsDict)
        resultDict=resultStatus.__dict__
        return json.dumps(resultDict,ensure_ascii=False)
    return json.dumps(rs.PARAM_ERROR,ensure_ascii=False)

@mc.route('/user/<int:userId>/consultList', methods = ['GET', 'POST'])
def getConsultsByUser(userId):
    sourceId=request.args.get('source_id')
    if userId:
        consuts=None
        if sourceId:
            consuts=Consult.getConsultsByUserId(userId,string.atoi(sourceId))
        else:
            consuts=Consult.getConsultsByUserId(userId)
        consutsDict=object2dict.objects2dicts(consuts)
        dataChangeService.setConsultsResult(consutsDict)

        resultStatus=rs.ResultStatus(rs.SUCCESS.status,rs.SUCCESS.msg,consutsDict)
        resultDict=resultStatus.__dict__
        return json.dumps(resultDict,ensure_ascii=False)
    return json.dumps(rs.PARAM_ERROR,ensure_ascii=False)
@mc.route('/consut/<int:consultId>/read', methods = ['GET', 'POST'])
def changeConsultRead(consultId):
    Consult.changeReadStatus(consultId)
    return json.dumps(rs.SUCCESS.__dict__,ensure_ascii=False)



