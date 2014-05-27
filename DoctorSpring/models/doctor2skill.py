# coding: utf-8
__author__ = 'Jeremy'

import sqlalchemy as sa

from database import Base ,db_session as session
from DoctorSpring.util.constant import ModelStatus, UserStatus



class Doctor2Skill(Base):
    __tablename__ = 'doctor2skill'
    __table_args__ = {
        'mysql_charset': 'utf8',
    }

    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    doctorId = sa.Column(sa.INTEGER)
    skillId = sa.Column(sa.INTEGER)
    status = sa.Column(sa.INTEGER)

    def __init__(self, doctorId=doctorId, skillId=skillId):
        self.doctorId = doctorId
        self.skillId = skillId
        self.status = ModelStatus.Normal

    @classmethod
    def save(cls, doctor2skill):
        if doctor2skill:
            session.add(doctor2skill)
            session.commit()
            session.flush()
