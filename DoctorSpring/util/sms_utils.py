__author__ = 'lichuan'
#!/usr/bin/env python
# coding: utf-8

from time import strftime, localtime
import urllib, urllib2, json
import hmac, hashlib

class RandCode(object):
    #APP_ID = '142196870000037017'

    APP_ID = '142196870000037017'
    APP_SECRET = 'c97905c7e47fd02222d3ab28fdd8a5ee'
    ACCESS_TOKEN = ''

    TOKEN_API = 'https://oauth.api.189.cn/emp/oauth2/v3/access_token'


    TEMPLATE_SEND_API = 'http://api.189.cn/v2/emp/templateSms/sendSms'
    #register verification code template
    TEMPLATE_ID_1 = '91002171'


    def __init__(self, app_id='', app_secret='', access_token=''):
        self.APP_ID = app_id or RandCode.APP_ID
        self.APP_SECRET = app_secret or RandCode.APP_SECRET
        self.ACCESS_TOKEN = access_token or self.__fetch_access_token()
        #self.RANDCODE_TOKEN = self.__fetch_randcode_token()

    def send_emp_sms(self,phone,template_id,template_param):
        result = False
        if self.ACCESS_TOKEN:
            data = {
                'app_id':self.APP_ID,
                'access_token':self.ACCESS_TOKEN,
                'acceptor_tel':phone,
                'template_id':template_id,
                'template_param':template_param,
                'timestamp':self.__date_time(),
                }
            data = self.__build_request_string(data)
            data = self.__data_sign(data)
            if data:
                res = self.__request_data('post', data, self.TEMPLATE_SEND_API)
                json_data = json.loads(res)
                print "sms return"
                if json_data['res_code'] == 0:
                    print "sms success"
                    result = True
                else:
                    print "sms error"



    def __request_data(self, method, data, url):
        if isinstance(data, dict):
            data = urllib.urlencode(data)
        if method == 'post':
            req = urllib2.Request(url, data)
        else:
            url = '%s?%s' % (url, data)
            req = urllib2.Request(url)
        return urllib2.urlopen(req).read()

    def __fetch_access_token(self):
        access_token = self.ACCESS_TOKEN
        if access_token == '':
            data = {
                'grant_type':'client_credentials',
                'app_id':self.APP_ID,
                'app_secret':self.APP_SECRET,
                }
            res = self.__request_data('post', data, self.TOKEN_API)
            json_data = json.loads(res)
            if json_data['res_code'] == '0':
                access_token = json_data['access_token']
            else:
                raise ValueError(json_data['res_message'])
        return access_token

    def __fetch_randcode_token(self):
        result = ''
        if self.ACCESS_TOKEN != '':
            data = {
                'app_id':self.APP_ID,
                'access_token':self.ACCESS_TOKEN,
                'timestamp':self.__date_time(),
                }
            data = self.__build_request_string(data)
            data = self.__data_sign(data)
            if data:
                res = self.__request_data('get', data, self.RANDCODE_TOKEN_API)
                json_data = json.loads(res)
                if json_data['res_code'] == 0:
                    result = json_data['token']
                else:
                    raise ValueError(json_data['res_message'])
        return result

    def __data_sign(self, data):
        result = ''
        if data:
            if isinstance(data, dict):
                data = self.__build_request_string(data)
                sign = hmac.new(self.APP_SECRET, urllib.urlencode(data), hashlib.sha1).digest()
            elif isinstance(data, unicode):
                sign = hmac.new(self.APP_SECRET, data, hashlib.sha1).digest()
            if data:
                result = "%s&sign=%s" % ( data, urllib.quote(sign.encode('base64').strip()) )
        return result

    def __build_request_string(self, dict):
        keys = dict.keys()
        keys.sort()
        return '&'.join([ key + "=" + dict[key] for key in keys ])

    def __date_time(self):
        return strftime("%Y-%m-%d %H:%M:%S", localtime())



# if __name__  == '__main__':
#     r = RandCode()
#     # r.send('phone number', 'http://yourdomain/rand_code.php', '3')
#     template_param = {'param1':'243455'}
#     r.send_emp_sms('13241541730', r.TEMPLATE_ID_1,json.dumps(template_param))
