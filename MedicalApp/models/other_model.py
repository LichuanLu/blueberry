# coding: utf-8
__author__ = 'chengc017'
import sqlalchemy as sa

from database import Base
class Message(Base):
    __tablename__ = 'message'
    __table_args__ = {
        'mysql_charset': 'utf8',
        }
    id= sa.Column(sa.BigInteger, primary_key = True, autoincrement = True)
    sender=sa.Column(sa.Integer)
    receiver=sa.Column(sa.Integer)
    title= sa.Column(sa.String(256))
    content=sa.Column(sa.String(51200))
    type=sa.Column(sa.Integer)#0:normal,1:system message,2:administrator message,3：分诊信息
    status=sa.Column(sa.Integer)#0:normal,1:delete,2:overdue
    createTime=sa.Column(sa.DateTime)
    startTime=sa.Column(sa.DateTime)
    endTime=sa.Column(sa.DateTime)
class Commend(Base):
    __tablename__ = 'commend'
    __table_args__ = {
        'mysql_charset': 'utf8',
    }
    id= sa.Column(sa.BigInteger, primary_key = True, autoincrement = True)
    observer=sa.Column(sa.Integer)
    receiver=sa.Column(sa.Integer )
    title=sa.Column(sa.String(256))
    picture=sa.Column(sa.String(256))
    content=sa.Column(sa.String(51200))
    create_time=sa.Column(sa.DateTime)
    type=sa.Column(sa.Integer)
    status=sa.Column(sa.Integer)
    parent_commend_id=sa.Column(sa.BigInteger)
class DiagnoseCommend(Commend):
    __tablename__ = 'diagnose_commend'
    diagnoseId=sa.Column(sa.BigInteger)
