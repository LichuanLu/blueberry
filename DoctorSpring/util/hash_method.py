# coding: utf-8
__author__ = 'chengc017'
import hashlib
def getHashPasswd(passwd):
    if passwd:
        return hashlib.md5(passwd).hexdigest().upper()
