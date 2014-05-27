# coding: utf-8
__author__ = 'Jeremy'

import sqlalchemy as sa

from database import Base
from database import db_session as session


class Hospital(Base):
    __tablename__ = 'hospital'
    __table_args__ = {
        'mysql_charset': 'utf8',
    }

    id = sa.Column(sa.Integer, primary_key = True, autoincrement = True)
    name = sa.Column(sa.String(255))
    address = sa.Column(sa.String(255))
    description = sa.Column(sa.TEXT)
    locationId = sa.Column(sa.INTEGER)   # Location表ID

    status = sa.Column(sa.INTEGER)


    def __init__(self, name=name, address=address, description=description,
                 locationId=locationId):
        self.name = name
        self.address = address
        self.description = description
        self.locationId = locationId


    def __repr__(self):
        return '<Post %s>' % (self.name)

    @classmethod
    def save(cls, hospital):
        if hospital:
            session.add(hospital)
            session.commit()
            session.flush()