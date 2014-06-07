# coding: utf-8
__author__ = 'chengc017'
from .constant import MessageType
class MessageContent(object):
    title=None
    content=None
    messageType=None
    def __init__(self,title,content,messageType):
        self.title=title
        self.content=content
        self.messageType=messageType

DefaultMessage=MessageContent('系统诊断通知','你好，系统中有一个新到的影像需要您来诊断！',MessageType.System)

