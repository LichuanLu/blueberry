# coding: utf-8
import config

__author__ = 'Jeremy'


import sys
reload(sys)
sys.setdefaultencoding('utf-8')
from flask import Flask
from flask_bootstrap import Bootstrap
from MedicalApp.views import user, frontend

app = Flask(__name__)
Bootstrap(app)
app.config.from_object(config)

def register_blueprints(app):
    app.register_blueprint(frontend)
    app.register_blueprint(user, url_prefix="/user")

register_blueprints(app)


