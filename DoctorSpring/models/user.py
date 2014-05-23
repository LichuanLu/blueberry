# coding: utf-8
__author__ = 'Jeremy'

import sqlalchemy as sa
from database import db_session as session

from database import Base


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
    status = sa.Column(sa.INTEGER)

