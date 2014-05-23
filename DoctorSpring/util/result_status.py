# coding: utf-8
__author__ = 'chengc017'
class ResultStatus(object):
    status=None
    msg=None
    data=None
    def __init__(self,status,msg,data=None):
        self.status=status
        self.msg=msg
        self.data=data
SUCCESS=ResultStatus(1,'success')
FAILURE=ResultStatus(2,'failure')
NO_LOGIN=ResultStatus(3,'no login')
NO_REGISTER=ResultStatus(4,'no register')
PERMISSION_DENY=ResultStatus(5,'permission deny')
NO_DATA=ResultStatus(6,'no data')
LOGIN_CHECK_FARLURE=ResultStatus(7,"login parameter error")
LOGIN_CHECK_SUCCESS=ResultStatus(8,"login success")
PARAM_ERROR=ResultStatus(9,"paramter error")
