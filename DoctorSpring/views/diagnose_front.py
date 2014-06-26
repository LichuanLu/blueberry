# coding: utf-8
__author__ = 'ccheng'

from flask import Flask, request, session, g, redirect, url_for, Blueprint, jsonify
from flask import abort, render_template, flash
from flask.ext.login import login_user, logout_user, current_user, login_required
from forms import LoginForm ,CommentsForm ,ReportForm
from DoctorSpring import lm
from database import  db_session
from sqlalchemy.exc import IntegrityError
from DoctorSpring.models import User,Patient,Doctor,Diagnose ,DiagnoseTemplate,Report,UserRole,Hospital
from DoctorSpring.models import User,Comment,Message,DiagnoseLog
from DoctorSpring.util import result_status as rs,object2dict ,constant
from DoctorSpring.util.authenticated import authenticated
from DoctorSpring.util.constant import MessageUserType,Pagger



import  data_change_service as dataChangeService
import json

import config
config = config.rec()

dfView = Blueprint('diagnose_front', __name__)

@dfView.route('/admin/fenzhen',  methods = ['GET', 'POST'])
def getDiagnosePage():
    hospitals=Hospital.getAllHospitals(db_session)
    hospitalsDict=object2dict.objects2dicts(hospitals)

    return render_template("adminFenzhen.html", datas=hospitalsDict)




