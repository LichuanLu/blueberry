# coding: utf-8
__author__ = 'Jeremy'

import sqlalchemy as sa

from database import Base ,db_session as session
from DoctorSpring.util.constant import ModelStatus, UserStatus



class Skill(Base):
    __tablename__ = 'skill'
    __table_args__ = {
        'mysql_charset': 'utf8',
    }

    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    name = sa.Column(sa.String(64))
    status = sa.Column(sa.INTEGER)

    def __init__(self, name=name):
        self.name = name
        self.status = ModelStatus.Normal

    @classmethod
    def save(cls, skill):
        if skill:
            session.add(skill)
            session.commit()
            session.flush()
