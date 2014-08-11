# coding: utf-8
__author__ = 'Jeremy'
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

from flask import Flask
from flask.ext.login import LoginManager
import config
from database import db_session


app = Flask(__name__)
app.debug = True
app.config.from_object(config)

@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()


import logging
from logging.handlers import RotatingFileHandler
file_handler = RotatingFileHandler('medical.log', maxBytes=1024 * 1024 * 100, backupCount=1)
file_handler.setLevel(logging.INFO)
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
file_handler.setFormatter(formatter)
app.logger.addHandler(file_handler)
logging.basicConfig(filename='medical_access.log',level=logging.DEBUG)


lm = LoginManager()
lm.init_app(app)


def register_blueprints(app):
    # Prevents circular imports
    from views import user_view
    from views import front
    from views import mc,uc,diagnoseView,dfView
    #from views import admin
    app.register_blueprint(user_view)
    app.register_blueprint(front)
    app.register_blueprint(mc)
    app.register_blueprint(uc)
    app.register_blueprint(diagnoseView)
    app.register_blueprint(dfView)

register_blueprints(app)