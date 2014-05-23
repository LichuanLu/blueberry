# coding: utf-8
__author__ = 'Jeremy'

import sqlalchemy as sa

from database import Base


class Post(Base):
    __tablename__ = 'pathology'
    __table_args__ = {
        'mysql_charset': 'utf8',
        }

    id = sa.Column(sa.Integer, primary_key = True, autoincrement = True)
    hospticalId = sa.Column(sa.INTEGER)    #医院ID
    diagnoseDocId = sa.Column(sa.INTEGER)  #诊断表ID
    diagnosePartId = sa.Column(sa.INTEGER)  #检查部位ID
    caseHistory = sa.Column(sa.TEXT)       #病史
    status = sa.Column(sa.INTEGER)      #标记状态 未提交，待审查，待诊断，待审核，结束



'''
    def __init__(self, title=title, content=content, origin_content=None,
                 created_date=None, update_date=None):
        self.title = title
        self.content = content
        self.update_date = update_date
        if created_date == None:
            self.created_date = time.time()
        else:
            self.created_date = created_date
        if origin_content == None:
            self.origin_content = content
        else:
            self.origin_content = origin_content


    def __repr__(self):
        return '<Post %s>' % (self.title)
'''