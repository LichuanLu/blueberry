import config

__author__ = 'Jeremy'
# coding: utf-8

from flask import session, abort


config = config.rec()


def on_finish():
    None

def currentUserGet():
    if 'user' in session:
        user = session['user']
        return user['username']
    else:
        return None

def currentUserSet(username):
    if username:
        session['user'] = dict({'username':username})
    else:
        session.pop('user',None)


def userAuth(username, password):
    return username == config.admin_username and password == config.admin_password

def isAdmin():
    return currentUserGet() == config.admin_username

def checkAdmin():
    if not isAdmin():
        abort(404)

def get_current_user():
    return currentUserGet()
