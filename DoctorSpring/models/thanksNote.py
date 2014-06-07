__author__ = 'chengc017'
# coding: utf-8
__author__ = 'chengc017'
import sqlalchemy as sa
from DoctorSpring.util.constant import MessageStatus,ModelStatus,Pagger
from datetime import datetime
from database import db_session as session


from database import Base
class ThanksNote(Base):
    __tablename__ = 'thanksNote'
    __table_args__ = {
        'mysql_charset': 'utf8',
        'mysql_engine': 'MyISAM',
    }
    id= sa.Column(sa.BigInteger, primary_key = True, autoincrement = True)
    sender=sa.Column(sa.Integer)
    receiver=sa.Column(sa.Integer)
    title= sa.Column(sa.String(256))
    content=sa.Column(sa.String(51200))
    status=sa.Column(sa.Integer)#0:normal,1:delete,2:overdue
    createTime=sa.Column(sa.DateTime)
    def __init__(self,sender,receiver,title,content):
        self.sender=sender
        self.receiver=receiver
        self.title=title
        self.content=content

        self.status=MessageStatus.Normal
        self.createTime=datetime.now()
    @classmethod
    def save(self,session,ThanksNote):
        if ThanksNote:
            session.add(ThanksNote)
            session.commit()
            session.flush()
    @classmethod
    def getThanksNoteByReceiver(cls,session,receiverId,pager=Pagger(1,20),status=ModelStatus.Normal):
        if receiverId is None or receiverId<1:
            return

        return session.query(ThanksNote).filter(ThanksNote.receiver==receiverId,ThanksNote.status==status).order_by(ThanksNote.createTime.desc()) \
            .offset(pager.getOffset()).limit(pager.getLimitCount()).all()

    @classmethod
    def getThanksNoteCountByReceiver(cls,session,receiverId,status=MessageStatus.Normal):
        if receiverId is None or receiverId<1:
            return

        return session.query(ThanksNote).filter(ThanksNote.receiver==receiverId,ThanksNote.status==status).count()
    @classmethod
    def getThanksNoteBySender(cls,senderId,status=ModelStatus.Normal):
        if senderId is None or senderId<1:
            return

        return session.query(ThanksNote).filter(ThanksNote.sender==senderId,ThanksNote.status==status) \
            .order_by(ThanksNote.createTime.desc()).all()



