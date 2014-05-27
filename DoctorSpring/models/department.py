# coding: utf-8
__author__ = 'Jeremy'

import sqlalchemy as sa

from database import Base ,db_session as session
from DoctorSpring.util.constant import ModelStatus



class Department(Base):
    __tablename__ = 'department'
    __table_args__ = {
        'mysql_charset': 'utf8',
    }

    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    name = sa.Column(sa.String(64))
    description = sa.Column(sa.String(255))
    status = sa.Column(sa.INTEGER)

    def __init__(self, name=name, description=description):
        self.name = name
        self.description = description
        self.status = ModelStatus.Normal

    @classmethod
    def save(cls, department):
        if department:
            session.add(department)
            session.commit()
            session.flush()
