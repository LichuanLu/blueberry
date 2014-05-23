# coding: utf-8
__author__ = 'Jeremy'


from flask  import Blueprint
from flask import render_template
from forms import PostForm

frontend = Blueprint('frontend', __name__)

@frontend.route('/index')
@frontend.route('/')
def home():
    return render_template("index.html")



