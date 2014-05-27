# coding: utf-8
__author__ = 'Jeremy'

import sqlalchemy as sa

from database import Base ,db_session as session
from DoctorSpring.util.constant import ModelStatus, UserStatus



class SkillRDoctor(Base):
    __tablename__ = 'skillRdoctor'
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
    def save(cls, skillRdoctor):
        if skillRdoctor:
            session.add(skillRdoctor)
            session.commit()
            session.flush()
