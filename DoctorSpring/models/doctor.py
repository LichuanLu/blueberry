# coding: utf-8
__author__ = 'chengc017'
# coding: utf-8

import sqlalchemy as sa

from database import Base,db_session as session
from DoctorSpring.util.constant import ModelStatus, UserStatus
from sqlalchemy.orm import relationship, backref
from DoctorSpring.models import User
import config


class Doctor(Base):
    __tablename__ = 'doctor'
    __table_args__ = {
        'mysql_charset': 'utf8',
    }

    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    userId = sa.Column(sa.Integer, sa.ForeignKey('user.id'))     #对应User表里的ID
    user = relationship("User", backref=backref('doctor', order_by=id))
    username = sa.Column(sa.String(64))
    identityPhone = sa.Column(sa.INTEGER)
    title = sa.Column(sa.String(64))    #职称
    hospitalId = sa.Column(sa.INTEGER,sa.ForeignKey('hospital.id'))  #医院ID
    hospital = relationship("Hospital", backref=backref('doctor', order_by=id))
    departmentId = sa.Column(sa.INTEGER,sa.ForeignKey('department.id'))  #科室ID
    department = relationship("Department", backref=backref('Doctor', order_by=id))

    doctorSkills = relationship("Doctor2Skill", order_by="Doctor2Skill.id", backref="Doctor")
    description = sa.Column(sa.TEXT)
    diagnoseCount = sa.Column(sa.INTEGER)   #统计，诊断量
    feedbackCount = sa.Column(sa.INTEGER)   #好评数
    auditCount = sa.Column(sa.INTEGER)      #审核量
    type = sa.Column(sa.INTEGER)
    status = sa.Column(sa.INTEGER)

    def __init__(self, userId=None):
        self.userId = userId
        self.title = config.DEFAULT_TITLE
        self.status = ModelStatus.Normal

    @classmethod
    def getById(cls,doctorId):
        if doctorId is None or doctorId<0:
            return
        return session.query(Doctor).filter(Doctor.id==doctorId,Doctor.status==ModelStatus.Normal).first()
    @classmethod
    def getByUserId(cls,userId):
        if userId is None or userId<0:
            return
        return session.query(Doctor).filter(Doctor.userId==userId,Doctor.status==ModelStatus.Normal).first()


    @classmethod
    def save(cls, doctor):
        if doctor:
            session.add(doctor)
            session.commit()
            session.flush()


    @classmethod
    def get_doctor_list(cls, hospitalId, sectionId, doctorname, pagger, recommended=False):
        # return session.query(Doctor).all()
         query = session.query(Doctor).join(User, Doctor.userId == User.id). \
            join(Doctor2Skill, Doctor.id == Doctor2Skill.doctorId). \
            join(Skill, Skill.id == Doctor2Skill.skillId). \
            filter(User.type == UserStatus.doctor, User.status == ModelStatus.Normal,
                   Doctor.status == ModelStatus.Normal)

         if hospitalId != 0:
            query = query.filter(Doctor.hospitalId == hospitalId)

         if sectionId != 0:
            query = query.filter(Doctor.sectionId == sectionId)

         if doctorname is not '':
            query = query.filter(Doctor.username == doctorname or Doctor.name == doctorname)

         if pagger is not None:
            query = query.offset(pagger.count).limit(pagger.pageSize).all()

         if(recommended):
             return query.first()

         return query



class Doctor2Skill(Base):
    __tablename__ = 'doctor2skill'
    __table_args__ = {
        'mysql_charset': 'utf8',
        'mysql_engine': 'MyISAM',
    }

    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)


    doctorId = sa.Column(sa.INTEGER, sa.ForeignKey('doctor.id'))
    doctor = relationship("Doctor", backref=backref('Doctor2skill', order_by=id))
    skillId = sa.Column(sa.INTEGER, sa.ForeignKey('skill.id'))
    skill = relationship("Skill", backref=backref('Doctor2skill', order_by=id))

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