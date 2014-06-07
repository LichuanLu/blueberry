import  functools
from flask import Flask, request, session, g, redirect, url_for, Blueprint, jsonify
from DoctorSpring.util import constant
from database import db_session
from DoctorSpring.models import UserRole
__author__ = 'chengc017'


NO_LOGIN_URL='user_view.login'
PERMISSION_DENY_URL='user_view.registerdoctorPage'
class authenticated(object):

    def __init__(self, auth_model,role=None):
        self.auth_model = auth_model
        self.role=role

    def __call__(self, method):

        @functools.wraps(method)
        def admin_wrapper(*args, **kwargs):
            userId = session['userId']
            if userId is None:
                redirect(url_for(NO_LOGIN_URL))
            elif self.role and UserRole.checkRole(db_session,userId,self.role):
                return method(*args, **kwargs)
            #there have some bug needs to be fixed
            # elif self.role !=None and  userinfo and int(userinfo['cross_share_grade']) == self.role:
            #     return method(_self, *args, **kwargs)
            else:
                redirect(url_for(PERMISSION_DENY_URL))

        wrapper = dict(admin=admin_wrapper)
        return wrapper[self.auth_model]