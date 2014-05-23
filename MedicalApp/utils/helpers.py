import config

__author__ = 'Jeremy'
# coding: utf-8

from hashlib import md5
import time

setting = config.rec()

def getDay(timestamp):
    FORY = '%d'
    #os.environ["TZ"] = config.default_timezone
    #time.tzset()
    str = time.strftime(FORY, time.localtime(timestamp))
    return str

def getMonth(timestamp):
    FORY = '%b'
    #os.environ["TZ"] = config.default_timezone
    #time.tzset()
    str = time.strftime(FORY, time.localtime(timestamp))
    return str

def getAvatar(email, size=48):
    return \
        'http://gravatar.com/avatar/%s?d=identicon&s=%d&d=http://feather.im/static/img/gravatar.png' \
        % (md5(email.strip().lower().encode('utf-8')).hexdigest(), size)



