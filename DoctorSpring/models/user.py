# coding: utf-8
__author__ = 'Jeremy'

import sqlalchemy as sa
from database import db_session as session

from database import Base
from DoctorSpring.util.constant import ModelStatus
from datetime import datetime


class User(Base):
    __tablename__ = 'User'
    __table_args__ = {
        'mysql_charset': 'utf8',
        }

    id = sa.Column(sa.Integer, primary_key = True, autoincrement = True)
    name = sa.Column(sa.String(255))
    password = sa.Column(sa.String(255))
    address = sa.Column(sa.String(255))
    email = sa.Column(sa.String(64))
    imagePath = sa.Column(sa.String(255))
    sex = sa.Column(sa.INTEGER)   # Location表ID


    status = sa.Column(sa.INTEGER)

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return unicode(self.id)

    def __init__(self, name=None, password=None):
        self.name = name
        self.password = password

    def __repr__(self):
        return '<User %r>' % (self.name)
    @classmethod
    def save(cls,user):
        if user:
            session.add(user)
            session.commit()
            session.flush()





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




