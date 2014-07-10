# coding: utf-8
__author__ = 'Jeremy'

import os.path

ROOT_DIR=os.path.dirname(__file__)

_DBUSER = "mduser"
_DBPASS = "mduser"
_DBNAME = "medicaldb"
_DBHOST = "localhost:3306"

ROOT_DIR=os.path.dirname(__file__)

#config
SECRET_KEY = 'flasksimplelaw'
SITE_TITLE = '易诊断'
SITE_URL = 'http://www.ezhenduan.com'
SITE_NAME = '易诊断'

#admin info
ADMIN_INFO = ''
ADMIN_EMAIL = 'admin@simplelaw.cn'
ADMIN_USERNAME = 'admin'


DEFAULT_FILE_STORAGE = 'filesystem'
UPLOADS_FOLDER = os.path.realpath('.') + '/static/'
FILE_SYSTEM_STORAGE_FILE_VIEW = 'static'

# User
DEFAULT_IMAGE = '/static/assets/image/young-m.png'
DEFAULT_TITLE = '待定'

class rec:
    pass

rec.database = 'mysql://%s:%s@%s/%s' % (_DBUSER, _DBPASS, _DBHOST, _DBNAME)
rec.description = u"易诊断"
rec.url = 'http://www.ezhenduan.com'
rec.paged = 8
rec.archive_paged = 20
rec.admin_username = 'admin'
rec.admin_email = 'admin@simplelaw.cn'
rec.admin_password = 'passw0rd'
rec.default_timezone = "Asia/Shanghai"


