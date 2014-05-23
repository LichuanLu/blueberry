# coding: utf-8
__author__ = 'Jeremy'

import os.path

_DBUSER = "ctt"
_DBPASS = "ctt"
_DBHOST = "localhost"
_DBNAME = "medicaldb"

#config
SECRET_KEY = 'flasksimplelaw'
SITE_TITLE = 'Welcome. | Simple LAW'
SITE_URL = 'http://www.simplelaw.cn'
SITE_NAME = 'simplelaw'

#admin info
ADMIN_INFO = ''
ADMIN_EMAIL = 'admin@simplelaw.cn'
ADMIN_USERNAME = 'admin'


DEFAULT_FILE_STORAGE = 'filesystem'
UPLOADS_FOLDER = os.path.realpath('.') + '/static/'
FILE_SYSTEM_STORAGE_FILE_VIEW = 'static'

class rec:
    pass

rec.database = 'mysql://%s:%s@%s/%s' % (_DBUSER, _DBPASS, _DBHOST, _DBNAME)
rec.description = u"simple law"
rec.url = 'http://www.simplelaw.cn'
rec.paged = 8
rec.archive_paged = 20
rec.admin_username = 'admin'
rec.admin_email = 'admin@simplelaw.cn'
rec.admin_password = 'passw0rd'
rec.default_timezone = "Asia/Shanghai"


