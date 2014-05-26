# coding: utf-8
__author__ = 'Jeremy'

from flask import Flask, request, session, g, redirect, url_for, Blueprint, jsonify
from flask import abort, render_template, flash
from flask.ext.login import login_user, logout_user, current_user, login_required
from forms import LoginForm1, RegisterForm, RegisterFormPatent, RegisterFormDoctor
from DoctorSpring import lm
from database import db_session
from sqlalchemy.exc import IntegrityError
from DoctorSpring.models import User, Patent, Doctor
from DoctorSpring.util import result_status as rs, object2dict,constant
from DoctorSpring.util.constant import UserStatus
from DoctorSpring.util.helper import get_name

import json

import config
config = config.rec()

user_view = Blueprint('user_view', __name__)


# @app.before_request
# def before_request():
#     g.user = current_user

@lm.user_loader
def load_user(id):
    return User.getById(int(id))


@user_view.route('/login.json', methods=['GET', 'POST'])
def login():
    form = LoginForm1(request.form)
    formResult = form.validate()
    if formResult.status == rs.SUCCESS.status:
        #session['remember_me'] = form.remember_me.data
        # login and validate the user...
        user = User.get_by_name(form.Username)
        login_user(user)
        flash("登陆成功")
        session['logged_in'] = True
        session['username'] = User.name
        return json.dumps(formResult.__dict__, ensure_ascii=False)
    return json.dumps(formResult.__dict__, ensure_ascii=False)

@user_view.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@user_view.route('/register/patient',  methods = ['GET', 'POST'])
def register_patient_page():
    return render_template("patientRegister.html")

@user_view.route('/register/doctor',  methods = ['GET', 'POST'])
def registerdoctorPage():
    return render_template("doctorRegister.html")


@user_view.route('/register/doctor.json',  methods = ['GET', 'POST'])
def register_doctor():
    form = RegisterFormDoctor(request.form)
    form_result = form.validate()

    if form_result.status == rs.SUCCESS.status:
        new_user = User(form.username, form.password)
        new_user.email = form.email
        new_user.phone = form.cellphone
        User.save(new_user)
        new_doctor = Doctor(new_user.id)
        new_doctor.identityPhone = form.identity_phone
        Doctor.save(new_doctor)
        login_user(new_user)
        session['logged_in'] = True
        session['username'] = get_name(new_user)
        flash('注册成功，跳转至首页')
        #return jsonify(form_result.__dict__)
    return jsonify(form_result.__dict__)

@user_view.route('/register/patient.json',  methods=['GET', 'POST'])
def register_patient():
    form = RegisterFormPatent(request.form)
    form_result = form.validate()
    if form_result.status == rs.SUCCESS.status:
        new_user = User(form.name, form.password)
        new_user.type = UserStatus.patent
        User.save(new_user)
        new_patient = Patent(new_user.id)
        Patent.save(new_patient)
        return json.dumps(form_result.__dict__,ensure_ascii=False)
    return json.dumps(form_result.__dict__,ensure_ascii=False)



