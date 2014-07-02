# coding: utf-8
__author__ = 'Jeremy'

import sqlalchemy as sa

from database import Base ,db_session as session
from DoctorSpring.util.constant import ModelStatus, UserStatus



class Location(Base):
    __tablename__ = 'location'
    __table_args__ = {
        'mysql_charset': 'utf8',
        'mysql_engine': 'MyISAM',
    }

    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    name = sa.Column(sa.String(64))
    status = sa.Column(sa.INTEGER)

    def __init__(self, name=name):
        self.name = name
        self.status = ModelStatus.Normal

    @classmethod
    def save(cls, location):
        if location:
            session.add(location)
            session.commit()
            session.flush()

    @staticmethod
    def getAllLocations(session):
        return session.query(Location).filter(Location.status==ModelStatus.Normal).all()