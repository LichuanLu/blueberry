# coding: utf-8
__author__ = 'ccheng'

import sqlalchemy as sa
from database import db_session as session
from werkzeug.security import generate_password_hash, check_password_hash
from database import Base
from DoctorSpring.util.constant import ModelStatus, PatientStatus
import config
from DoctorSpring.util.constant import ModelStatus
from datetime import datetime


class User(Base):
    __tablename__ = 'User'
    __table_args__ = {
        'mysql_charset': 'utf8',
    }

    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    name = sa.Column(sa.String(255))
    account= sa.Column(sa.String(255))
    accountType=sa.Column(sa.String(255))
    password = sa.Column(sa.String(255))
    address = sa.Column(sa.String(255))
    email = sa.Column(sa.String(64))
    mobile = sa.Column(sa.String(32))
    imagePath = sa.Column(sa.String(255))
    sex = sa.Column(sa.INTEGER)   # Location表ID
    phone = sa.Column(sa.INTEGER)
<<<<<<< HEAD

    type=sa.Column(sa.Integer)  # 0:patent,1:doctor
    status = sa.Column(sa.INTEGER)  # 0:normal,1:delete,2:overdue

    def set_password(self, password):
        self.password = generate_password_hash(password)

=======
    
    type=sa.Column(sa.Integer)  # 0:patent,1:doctor
    status = sa.Column(sa.INTEGER)  # 0:normal,1:delete,2:overdue

    def set_password(self, password):
        self.password = generate_password_hash(password)

>>>>>>> d63de41b2967f75b3e878bd2be836d1e4065cfb7
    def check_password(self, password):
        return check_password_hash(self.password , password)

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return unicode(self.id)

    def __init__(self, name=None, password=None):
        if '@' in name:
            self.email = name
        else:
            self.phone = name
        self.password = generate_password_hash(password)
        self.imagePath = config.DEFAULT_IMAGE
        self.status = ModelStatus.Normal

    def __repr__(self):
        return '<User %r>' % (self.name)

    @classmethod
    def save(cls, user):
        if user:
            session.add(user)
            session.commit()
            session.flush()
    @classmethod
    def getById(cls, userId):
        if userId is None or userId < 1:
            return
        return session.query(User).filter(User.id==userId,User.status==ModelStatus.Normal).first()
<<<<<<< HEAD

    @classmethod
    def get_name(cls, user):
        if user is None:
            return ''
        if user.name is not None:
            return user.name

        if user.email is not None:
            return user.email

=======

    @classmethod
    def get_name(cls, user):
        if user is None:
            return ''
        if user.name is not None:
            return user.name

        if user.email is not None:
            return user.email

>>>>>>> d63de41b2967f75b3e878bd2be836d1e4065cfb7
        if user.phone is not None:
            return user.phone

    @classmethod
    def get_by_name(cls, user_name):
        if user_name is None or user_name < 1:
            return
        if '@' in user_name:
            return session.query(User).filter(User.email == user_name, User.status == ModelStatus.Normal).first()
        else:
            return session.query(User).filter(User.phone == user_name, User.status == ModelStatus.Normal).first()



class UserFavorites(Base):
    __tablename__ = 'user_favorites'
    __table_args__ = {
        'mysql_charset': 'utf8',
        }
    id = sa.Column(sa.Integer, primary_key = True, autoincrement = True)
    userId = sa.Column(sa.Integer)
    doctorId = sa.Column(sa.Integer)
    docId = sa.Column(sa.Integer)
    hospitalId=sa.Column(sa.Integer)
    createDate=sa.Column(sa.DateTime)
    type = sa.Column(sa.INTEGER)
    status = sa.Column(sa.INTEGER)

    def __init__(self,userId,type,doctorId=None,hospitalId=None,docId=None):
        self.userId=userId
        self.doctorId=doctorId
        self.hospitalId=hospitalId
        self.docId=docId
        self.status=ModelStatus
        self.type=type
        self.createDate=datetime.now()

    @classmethod
    def save(cls,userFavorites):
        if userFavorites:
            session.add(userFavorites)
            session.commit()
            session.flush()
    @classmethod
    def cancleFavorites(cls,userFavoritesId):
        if userFavoritesId:
            user=session.query(UserFavorites).filter(UserFavorites.id==userFavoritesId).first()
            if user:
                user.status=ModelStatus.Del
                session.commit()
    @classmethod
    def getUserFavorties(cls,userId,type,status=None):
        if userId:
            if type:
                if status:
                    return session.query(UserFavorites).filter(UserFavorites.userId==userId,UserFavorites.type==type,UserFavorites.status==status).all()
                else:
                    return session.query(UserFavorites).filter(UserFavorites.userId==userId,UserFavorites.type==type,UserFavorites.status==ModelStatus.Normal).all()

            else:
                if status:
                    return session.query(UserFavorites).filter(UserFavorites.userId==userId,UserFavorites.status==status).all()
                else:
                    return session.query(UserFavorites).filter(UserFavorites.userId==userId,UserFavorites.status==ModelStatus.Normal).all()

