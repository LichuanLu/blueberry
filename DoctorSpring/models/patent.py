# coding: utf-8
__author__ = 'chengc017'

import sqlalchemy as sa

from database import Base ,db_session as session


class Patent(Base):
    __tablename__ = 'patent'
    __table_args__ = {
        'mysql_charset': 'utf8',
        }

    id = sa.Column(sa.Integer, primary_key = True, autoincrement = True)
    userID = sa.Column(sa.INTEGER)
    locationId = sa.Column(sa.INTEGER)     #所在地ID
    identityCode = sa.Column(sa.String(64))
    gender = sa.Column(sa.INTEGER)
    birthDate = sa.Column(sa.DATE)
    name = sa.Column(sa.String(64))
    status = sa.Column(sa.INTEGER)

    def __init__(self, userId=None):
        self.userID = userId
    @classmethod
    def save(cls,patient):
        if patient:
            session.add(patient)
            session.commit()
            session.flush()

'''
    def __repr__(self):
        return '<Post %s>' % (self.title)
'''