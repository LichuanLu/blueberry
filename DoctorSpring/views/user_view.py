# coding: utf-8
__author__ = 'Jeremy'

from flask import Flask, request, session, g, redirect, url_for, Blueprint, jsonify
from flask import abort, render_template, flash
from flask.ext.login import login_user, logout_user, current_user, login_required
from forms import LoginForm, RegisterFormPatent, RegisterFormDoctor
from DoctorSpring import lm
from database import db_session
from sqlalchemy.exc import IntegrityError
from DoctorSpring.models import User, Patient, Doctor
from DoctorSpring.util import result_status as rs, object2dict,constant
from DoctorSpring.util.constant import UserStatus

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
            #return jsonify(formResult.__dict__)
    return jsonify(formResult.__dict__)

@user_view.route('/logout')
def logout():
    session['logged_in'] = False
    session['username'] = ''
    logout_user()
    return render_template("home.html")


@user_view.route('/register/patient',  methods = ['GET', 'POST'])
def register_patient_page():
    return render_template("patientRegister.html")

@user_view.route('/register/doctor',  methods = ['GET', 'POST'])
def registerDoctorPage():
    return render_template("doctorRegister.html")


@user_view.route('/register/doctor.json',  methods = ['GET', 'POST'])
def registerDoctor():
    error = None
    temp=request.form
    form = RegisterForm(request.form, csrf_enabled=False)
    print form.name.data
    if request.method == "POST" and form.validate():
        print form.username.data

        new_user = User(form.username.data, form.password.data)
        try:
            db_session.add(new_user)
            db_session.commit()
            flash('Thanks for registering. Please login.')
            db_session.flush()
            new_patient = Patent(new_user.id)
            db_session.add(new_patient)
            db_session.commit()
            return jsonify({'code': 0,  'message' : "success", 'data' : ""})
        except IntegrityError:
            error = 'Oh no! That username and/or email already exist. Please try again.'
    else:
        flash_errors(form)
    return render_template('patientRegister.html', form=form, error=error)


@user_view.route('/register/patient.json',  methods = ['GET', 'POST'])
def register():
    error = None
    form = RegisterForm(request.form, csrf_enabled=False)
    if request.method == "POST" and form.validate():
        print form.name.data

        new_user = User(form.name.data, form.password.data)
        try:
            db_session.add(new_user)
            db_session.commit()
            flash('Thanks for registering. Please login.')
            db_session.flush()
            new_patient = Patent(new_user.id)
            db_session.add(new_patient)
            db_session.commit()
            return jsonify({'code': 0,  'message' : "success", 'data' : ""})
        except IntegrityError:
            error = 'Oh no! That username and/or email already exist. Please try again.'
    else:
        flash_errors(form)
    return render_template('patientRegister.html', form=form, error=error)


def flash_errors(form):
    for field, errors in form.errors.items():
        for error in errors:
            flash(u"Error in the %s field - %s" % (
                getattr(form, field).label.text,error), 'error')