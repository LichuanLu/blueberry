# coding: utf-8
__author__ = 'chengc017'
import sqlalchemy as sa
from DoctorSpring.util.constant import MessageStatus
from datetime import datetime
from database import db_session as session


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
    def __init__(self,sender,receiver,title,content,type):
        self.sender=sender
        self.receiver=receiver
        self.title=title
        self.content=content
        self.type=type
        self.status=MessageStatus.Normal
        self.createTime=datetime.now()
    @classmethod
    def save(self,message):
        if message:
            session.add(message)
            session.commit()
            session.flush()
    @classmethod
    def getMessageByReceiver(cls,receiverId,status=MessageStatus.Normal):
        if receiverId is None or receiverId<1:
            return

        return session.query(Message).filter(Message.receiver==receiverId,Message.status==status)\
            .order_by(Message.createTime.desc()).all()

    @classmethod
    def getMessageCountByReceiver(cls,receiverId,status=MessageStatus.Normal):
        if receiverId is None or receiverId<1:
            return

        return session.query(Message).filter(Message.receiver==receiverId,Message.status==status).count()
    @classmethod
    def getMessagesBySender(cls,senderId,status=MessageStatus.Normal):
        if senderId is None or senderId<1:
            return

        return session.query(Message).filter(Message.sender==senderId,Message.status==status)\
            .order_by(Message.createTime.desc()).all()
    @classmethod
    def remarkMessage(cls,messageId,status=MessageStatus.Readed):
        if messageId is None or messageId<1:
            return False
        message=session.query(Message).filter(Message.id==messageId,MessageStatus.Normal).update({
            Message.status:status
        })
        if message:
            return True
        return False

