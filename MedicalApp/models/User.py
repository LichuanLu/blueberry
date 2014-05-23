# coding: utf-8
__author__ = 'Jeremy'

import sqlalchemy as sa

from database import Base


class Post(Base):
    __tablename__ = 'User'
    __table_args__ = {
        'mysql_charset': 'utf8',
        }

    id = sa.Column(sa.Integer, primary_key = True, autoincrement = True)
    name = sa.Column(sa.String(255))
    address = sa.Column(sa.String(255))
    email = sa.Column(sa.String(64))
    sex = sa.Column(sa.INTEGER)   # Location表ID


    status = sa.Column(sa.INTEGER)


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




'''
    def __init__(self, title=title, content=content, origin_content=None,
                 created_date=None, update_date=None):
        self.title = title
        self.content = content
        self.update_date = update_date
        if created_date == None:
            self.created_date = time.time()
        else:
            self.created_date = created_date
        if origin_content == None:
            self.origin_content = content
        else:
            self.origin_content = origin_content


    def __repr__(self):
        return '<Post %s>' % (self.title)
'''