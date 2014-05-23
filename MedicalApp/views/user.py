import config

__author__ = 'Jeremy'
# coding: utf-8

from flask  import session, redirect,url_for,Blueprint
from flask import render_template,flash
from MedicalApp.views.forms import PostForm


config = config.rec()

user = Blueprint('user', __name__)


@user.route('/logout')
def logout():
    session.pop('user',None)
    return redirect('/login')

@user.route('/login', methods=['GET', 'POST'])
def login():
    def index():
        form = PostForm()
        if form.validate_on_submit():

            flash('Your post is now live!')
            return redirect(url_for('/'))
        return render_template("login.html",
                               form = form)
