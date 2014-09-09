# coding: utf-8
__author__ = 'chengc017'

import sqlalchemy as sa
from sqlalchemy.orm import relationship, backref
from database import Base
from database import db_session as session
from DoctorSpring.util import constant


class Hospital(Base):
    __tablename__ = 'hospital'
    __table_args__ = {
        'mysql_charset': 'utf8',
        'mysql_engine': 'MyISAM',
    }

    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    name = sa.Column(sa.String(255))
    address = sa.Column(sa.String(255))
    description = sa.Column(sa.TEXT)
    locationId = sa.Column(sa.Integer, sa.ForeignKey('location.id'))   # Location表ID
    location = relationship("Location", backref=backref('hospital', order_by=id))

    type = sa.Column(sa.INTEGER)
    level = sa.Column(sa.INTEGER)

    status = sa.Column(sa.INTEGER)


    def __init__(self, name=name, address=address, description=description,
                 locationId=locationId):
        self.name = name
        self.address = address
        self.description = description
        self.locationId = locationId
        self.status = constant.ModelStatus.Normal


    def __repr__(self):
        return '<Post %s>' % (self.name)

    @classmethod
    def save(cls, hospital):
        if hospital:
            session.add(hospital)
            session.commit()
            session.flush()
    @staticmethod
    def getAllHospitals(session):
        return session.query(Hospital).filter(Hospital.status==constant.ModelStatus.Normal).all()
    @staticmethod
    def updateHospital(hospital):
        if hospital is None or hospital.id is None:
            return
        hospitalNeedChange=session.query(Hospital).filter(Hospital.id==hospital.id,Hospital.status==constant.ModelStatus.Normal).first()
        if hospitalNeedChange is None:
            return
        if hospital.name:
            hospitalNeedChange.name=hospital.name
        if hospital.address:
            hospitalNeedChange.address=hospital.address
        session.commit()
        session.flush()

