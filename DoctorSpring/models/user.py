# coding: utf-8
__author__ = 'ccheng'

import sqlalchemy as sa
from database import db_session as session
from werkzeug.security import generate_password_hash, check_password_hash
from database import Base
from DoctorSpring.util.constant import ModelStatus, PatientStatus,UserFavoritesType
import config
from DoctorSpring.util.constant import ModelStatus
from datetime import datetime
from sqlalchemy.orm import relationship,backref


class User(Base):
    __tablename__ = 'user'
    __table_args__ = {
        'mysql_charset': 'utf8',
        'mysql_engine': 'MyISAM',
    }

    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    name = sa.Column(sa.String(255))
    account= sa.Column(sa.String(255))
    accountType=sa.Column(sa.String(255))
    password = sa.Column(sa.String(255))
    address = sa.Column(sa.String(255))
    email = sa.Column(sa.String(64))
    imagePath = sa.Column(sa.String(255))
    sex = sa.Column(sa.INTEGER)   # Location表ID
    phone = sa.Column(sa.INTEGER)
    type=sa.Column(sa.Integer)  # 0:patent,1:doctor
    status = sa.Column(sa.INTEGER)  # 0:normal,1:delete,2:overdue

    def set_password(self, password):
        self.password = generate_password_hash(password)

    
    type=sa.Column(sa.Integer)  # 0:patent,1:doctor
    status = sa.Column(sa.INTEGER)  # 0:normal,1:delete,2:overdue

    def set_password(self, password):
        self.password = generate_password_hash(password)


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


    @classmethod
    def get_name(cls, user):
        if user is None:
            return ''
        if user.name is not None:
            return user.name

        if user.email is not None:
            return user.email

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

class UserRole(Base):
    __tablename__ = 'user_role'
    __table_args__ = {
        'mysql_charset': 'utf8',
        'mysql_engine': 'MyISAM',

    }
    id = sa.Column(sa.Integer, primary_key = True, autoincrement = True)
    userId = sa.Column(sa.Integer)
    roleId= sa.Column(sa.String(30))

    @staticmethod
    def checkRole(session,userId,roleId):
        if userId and roleId:
           return session.query(UserRole).filter(UserRole.userId==userId,UserRole.roleId==roleId).count()>0
        else:
            return False
class Role(Base):
    __tablename__ = 'role'
    __table_args__ = {
        'mysql_charset': 'utf8',
        'mysql_engine': 'MyISAM',

    }
    id = sa.Column(sa.Integer, primary_key = True, autoincrement = True)
    roleName= sa.Column(sa.String(30))



class UserFavorites(Base):
    __tablename__ = 'user_favorites'
    __table_args__ = {
        'mysql_charset': 'utf8',
        'mysql_engine': 'MyISAM',

    }
    id = sa.Column(sa.Integer, primary_key = True, autoincrement = True)
    userId = sa.Column(sa.Integer)
    doctorId = sa.Column(sa.Integer,sa.ForeignKey('doctor.id'))
    doctor = relationship("Doctor", backref=backref('user_favorites', order_by=id))
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
        self.status=ModelStatus.Normal
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
    @staticmethod
    def checkUerFavorties(session,userId,type,favoritesObjectId):
        if type is None:
            return False
        query=session.query(UserFavorites.id).filter(UserFavorites.userId==userId,UserFavorites.status==ModelStatus.Normal)
        if type==UserFavoritesType.Doctor:
            query.filter(UserFavorites.type==type,UserFavorites.doctorId==favoritesObjectId)
        if type==UserFavoritesType.Hospital:
            query.filter(UserFavorites.type==type,UserFavorites.hospitalId==favoritesObjectId)
        results=query.all()
        if results and len(results)==1:
            return True
        return False
    @staticmethod
    def getUerFavortiesByDelStatus(session,userId,type,favoritesObjectId):
        if type is None:
            return False
        query=session.query(UserFavorites).filter(UserFavorites.userId==userId,UserFavorites.status==ModelStatus.Del)
        if type==UserFavoritesType.Doctor:
            query.filter(UserFavorites.type==type,UserFavorites.doctorId==favoritesObjectId)
        if type==UserFavoritesType.Hospital:
            query.filter(UserFavorites.type==type,UserFavorites.hospitalId==favoritesObjectId)
        result=query.first()
        return result



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

