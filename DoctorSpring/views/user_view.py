# coding: utf-8
__author__ = 'Jeremy'

from flask import Flask, request, session, g, redirect, url_for, Blueprint, jsonify
from flask import abort, render_template, flash
from flask.ext.login import login_user, logout_user, current_user, login_required
from forms import LoginForm, RegisterFormPatent, RegisterFormDoctor
from DoctorSpring import lm
from database import db_session
from sqlalchemy.exc import IntegrityError
from DoctorSpring.models import User, Patient, Doctor, UserRole, Doctor2Skill
from DoctorSpring.util import result_status as rs, object2dict,constant
from DoctorSpring.util.constant import UserStatus, RoleId, ModelStatus

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
    form = LoginForm(request.form)
    formResult = form.validate()
    if formResult.status == rs.SUCCESS.status:
        #session['remember_me'] = form.remember_me.data
        # login and validate the user...
        user = User.get_by_name(form.username)
        if user is not None:
            login_session(user)
            formResult.msg = request.host_url + "homepage"
        else:
            formResult = rs.LOGIN_CHECK_FARLURE

    return jsonify(formResult.__dict__)

@user_view.route('/logout')
def logout():
    session['logged_in'] = False
    session['username'] = None
    session['userId'] = None
    logout_user()
    return redirect('/homepage')

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
        new_user.type = UserStatus.doctor
        new_user.status = ModelStatus.Draft
        User.save(new_user)
        new_doctor = Doctor(new_user.id)
        new_doctor.username = form.real_name
        new_doctor.identityPhone = form.identity_phone
        Doctor.save(new_doctor)

        new_doctor2skill = Doctor2Skill(new_doctor.id, 1)
        Doctor2Skill.save(new_doctor2skill)

        new_userrole = UserRole(new_user.id, RoleId.Doctor)
        UserRole.save(new_userrole)

    return jsonify(form_result.__dict__)

@user_view.route('/register/patient.json',  methods=['GET', 'POST'])
def register_patient():
    form = RegisterFormPatent(request.form)
    form_result = form.validate()
    if form_result.status == rs.SUCCESS.status:
        new_user = User(form.name, form.password)
        new_user.type = UserStatus.patent
        User.save(new_user)
        new_patient = Patient(new_user.id)
        new_userrole = UserRole(new_user.id, RoleId.Patient)
        UserRole.save(new_userrole)
        Patient.save(new_patient)
        login_session(new_user)
        form_result.msg = request.host_url + 'homepage'
        return jsonify(form_result.__dict__,ensure_ascii=False)

    return jsonify(form_result.__dict__,ensure_ascii=False)



def login_session(user):
    login_user(user)
    session['logged_in'] = True
    session['username'] = User.get_name(user)
    session['userId'] = User.get_id(user)
    flash('注册成功，跳转至首页')