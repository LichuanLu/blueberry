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
    diagnoseId =sa.Column(sa.Integer)
    doctorId=sa.Column(sa.Integer )
    title=sa.Column(sa.String(256))
    content=sa.Column(sa.String(51200))
    createTime=sa.Column(sa.DateTime)
    updateTime=sa.Column(sa.DateTime)
    type= sa.Column(sa.Integer)#type:1doctor为发起者，type=0，user为发起者
    status=sa.Column(sa.Integer)    #2表示已读
    parent_id=sa.Column(sa.BigInteger)
    source_id=sa.Column(sa.BigInteger)#原始咨询的id，冗余，为了快速的找到一组讨论的咨询
    def __init__(self,userId,doctorId,title,content,parent_id=-1,source_id=-1,type=0):
        self.userId=userId
        self.doctorId=doctorId
        #self.title=title
        self.title=title
        self.content=content
        self.updateTime=datetime.now()
        self.createTime=datetime.now()

        self.status=constant.ModelStatus.Normal
        self.parent_id=parent_id
        self.source_id=source_id
        self.type=type
    @classmethod
    def save(cls,consult):
        if consult:
            session.add(consult)

            if consult.source_id!=None and consult.source_id!=-1:
                source=Consult.getById(consult.source_id)
                source.updateTime=datetime.now()
            session.commit()
            session.flush()


    @classmethod
    def getById(cls,id):
        if id is None:
            return
        return session.query(Consult).filter(Consult.id==id).first()
    @classmethod
    def getConsultsByDoctorId(cls,doctorId,sourceId=None):
        if doctorId is None:
            return
        if sourceId:
            return session.query(Consult).filter(Consult.doctorId==doctorId,Consult.source_id==sourceId,Consult.status!=ModelStatus.Del) \
                .order_by(Consult.updateTime.desc()).all()
        else:
            return session.query(Consult).filter(Consult.doctorId==doctorId,Consult.status!=ModelStatus.Del,Consult.source_id==-1). \
                order_by(Consult.updateTime.desc()).all()
    @classmethod
    def getConsultsByUserId(cls,userId,sourceId=None):
        if userId is None:
            return
        if sourceId:
            return session.query(Consult).filter(Consult.userId==userId,Consult.source_id==sourceId,Consult.status!=ModelStatus.Del)\
                .order_by(Consult.updateTime.desc()).all()
        else:
            return session.query(Consult).filter(Consult.userId==userId,Consult.status!=ModelStatus.Del,Consult.source_id==-1)\
                .order_by(Consult.updateTime.desc()).all()
    @classmethod
    def getConsultsBySourceId(cls,sourceId):
        if sourceId is None:
            return
        return session.query(Consult).filter(Consult.source_id==sourceId,Consult.status!=ModelStatus.Del).order_by(Consult.createTime.desc()).all()
    @classmethod
    def changeReadStatus(cls,id):
        if id is None:
            return
        consult=session.query(Consult).filter(Consult.id==id).first()
        if constant:
            consult.status=2#标记为已读
            session.commit()



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
        self.status=constant.ModelStatus.Draft
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
        return session.query(Comment).filter(Comment.status==status,Comment.type==type).order_by(Comment.createTime.desc()).limit(6).all()

    @classmethod
    def updateComment(cls,id,status=ModelStatus.Normal):
        comment=session.query(Comment).filter(Comment.id==id).first()
        if comment:
            if status or status==ModelStatus.Normal:
                comment.status=status
            return session.commit()
    @classmethod
    def getCommentsByDraft(cls,pagger=constant.Pagger(1,20)):
        return session.query(Comment).filter(Comment.status==ModelStatus.Draft).offset(pagger.getOffset()).limit(pagger.getLimitCount()).all()