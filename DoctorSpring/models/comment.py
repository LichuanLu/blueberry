# coding: utf-8
__author__ = 'chengc017'
import sqlalchemy as sa
from datetime import datetime
from DoctorSpring.util import constant
from database import db_session as session
from DoctorSpring.util.constant import ModelStatus,CommentType

from database import Base
class Consult(Base):
    __tablename__ = 'consult'
    __table_args__ = {
        'mysql_charset': 'utf8',
        'mysql_engine': 'MyISAM',

    }
    id= sa.Column(sa.BigInteger, primary_key = True, autoincrement = True)
    userId=sa.Column(sa.Integer)
    doctorId=sa.Column(sa.Integer )
    title=sa.Column(sa.String(256))
    content=sa.Column(sa.String(51200))
    createTime=sa.Column(sa.DateTime)
    status=sa.Column(sa.Integer)
    def __init__(self,userId,doctorId,title,content):
        self.userId=userId
        self.doctorId=doctorId
        #self.title=title
        self.title=title
        self.content=content
        self.createTime=datetime.now()
        self.status=constant.ModelStatus.Normal
    @classmethod
    def save(cls,consult):
        if consult:
            session.add(consult)
            session.commit()
            session.flush()
    @classmethod
    def getConsultsByDoctorId(cls,doctorId):
        if doctorId is None:
            return
        return session.query(Consult).filter(Consult.doctorId==doctorId,Consult.status==ModelStatus.Normal).all()
    @classmethod
    def getConsultsByUserId(cls,userId):
        if userId is None:
            return
        return session.query(Consult).filter(Consult.userId==userId,Consult.status==ModelStatus.Normal).all()


class Comment(Base):

    __tablename__ = 'comment'
    __table_args__ = {
        'mysql_charset': 'utf8',
        'mysql_engine': 'MyISAM',
        }
    id= sa.Column(sa.BigInteger, primary_key = True, autoincrement = True)
    observer=sa.Column(sa.Integer)
    receiver=sa.Column(sa.Integer )
    title=sa.Column(sa.String(256))
    content=sa.Column(sa.String(51200))
    createTime=sa.Column(sa.DateTime)
    type=sa.Column(sa.Integer)
    status=sa.Column(sa.Integer)
    parent_commend_id=sa.Column(sa.BigInteger)
    diagnoseId=sa.Column(sa.BigInteger)
    def __init__(self,observer,receiver,diagnoseId,content):
        self.observer=observer
        self.receiver=receiver
        #self.title=title
        self.diagnoseId=diagnoseId
        self.content=content
        self.createTime=datetime.now()
        self.status=constant.ModelStatus.Normal
        self.type=constant.CommentType.DiagnoseComment
    @classmethod
    def getCommentByUser(cls,observerId,status=ModelStatus.Normal,type=CommentType.Normal):
        return session.query(Comment).filter(Comment.observer == observerId,Comment.status==status,Comment.type==type).all()
    @classmethod
    def getCommentByReceiver(cls,receiverId,status=ModelStatus.Normal,type=CommentType.Normal,pagger=constant.Pagger(1,20)):
        return session.query(Comment).filter(Comment.receiver==receiverId,Comment.status==status,Comment.type==type).offset(pagger.getOffset())\
            .limit(pagger.getLimitCount()).all()
    @classmethod
    def getCommentBydiagnose(cls,diagnoseId,status=ModelStatus.Normal,type=CommentType.Normal):
        return session.query(Comment).filter(Comment.diagnoseId==diagnoseId,Comment.status==status,Comment.type==type).all()

    @classmethod
    def existCommentBydiagnose(cls,diagnoseId,status=ModelStatus.Normal,type=CommentType.Normal):
        if diagnoseId is None:
            return False
        return session.query(Comment).filter(Comment.diagnoseId==diagnoseId,Comment.status==status,Comment.type==type).count()>0
    @classmethod
    def getCountByReceiver(cls,receiverId,type=CommentType.DiagnoseComment):
        if receiverId is None:
            return
        return session.query(Comment.id).filter(Comment.receiver==receiverId,Comment.type==type,Comment.status==ModelStatus.Normal).count()
    @classmethod
    def getRecentComments(cls,status=ModelStatus.Normal,type=CommentType.DiagnoseComment):
        return session.query(Comment).filter(Comment.status==status,Comment.type==type).order_by(Comment.createTime.desc()).limit(3).all()
