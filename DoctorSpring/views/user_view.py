# coding: utf-8
__author__ = 'Jeremy'

from flask import Flask, request, session, g, redirect, url_for, Blueprint, jsonify
from flask import abort, render_template, flash
from flask.ext.login import login_user, logout_user, current_user, login_required
from forms import LoginForm, RegisterForm
from DoctorSpring import lm
from database import  db_session
from sqlalchemy.exc import IntegrityError
from DoctorSpring.models import User,Patent

import config
config = config.rec()

user_view = Blueprint('user_view', __name__)


# @app.before_request
# def before_request():
#     g.user = current_user

@lm.user_loader
def load_user(id):
    return User.query.get(int(id))
@user_view.route('/login.json', methods = ['GET', 'POST'])
def login():
    if g.user is not None and g.user.is_authenticated():
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        #session['remember_me'] = form.remember_me.data
        # login and validate the user...
        login_user(User)
        flash("Logged in successfully.")
        session['logged_in'] = True
        return jsonify({'code': 0,  'message' : "success"})
    return render_template("login.html", form=form)


@user_view.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@user_view.route('/register/patient',  methods = ['GET', 'POST'])
def registerPatientPage():
    return render_template("patientRegister.html")

@user_view.route('/register/doctor',  methods = ['GET', 'POST'])
def registerDoctorPage():
    return render_template("doctorRegister.html")


@user_view.route('/register/doctor.json',  methods = ['GET', 'POST'])
def registerDoctor():
    error = None
    form = RegisterForm(request.form, csrf_enabled=False)
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