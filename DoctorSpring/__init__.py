# coding: utf-8
__author__ = 'Jeremy'
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

from flask import Flask
from flask.ext.login import LoginManager
import config


app = Flask(__name__)
app.config.from_object(config)


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