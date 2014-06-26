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
SUCCESS=ResultStatus(0,'success')
FAILURE=ResultStatus(1,'failure')
NO_LOGIN=ResultStatus(2,'no login')
NO_REGISTER=ResultStatus(3,'no register')
PERMISSION_DENY=ResultStatus(4,'permission deny')
NO_DATA=ResultStatus(5,'no data')
LOGIN_CHECK_FARLURE=ResultStatus(6,"login parameter error")
LOGIN_CHECK_SUCCESS=ResultStatus(7,"login success")
PARAM_ERROR=ResultStatus(8,"paramter error")




