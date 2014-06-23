#coding=utf8
import time

from oss.oss_api import *


from oss.oss_xml_handler import *
import  hashlib
__author__ = 'chengc017'


HOST = "oss.aliyuncs.com"
WEB_HOST="oss-cn-hangzhou.aliyuncs.com"
ACCESS_ID = "5XxlKb2HfhZWlyLY"
SECRET_ACCESS_KEY = "SuqEzwOL5Pcl8VZZMgl0cPsgQqboDh"
#ACCESS_ID and SECRET_ACCESS_KEY 默认是空，请填入您申请的正确的ID和KEY.
def uploadFile(diagnoseId,fileName):
    if len(ACCESS_ID) == 0 or len(SECRET_ACCESS_KEY) == 0:
        print "Please make sure ACCESS_ID and SECRET_ACCESS_KEY are correct in ", __file__ , ", init are empty!"
        exit(0)
    oss = OssAPI(HOST, ACCESS_ID, SECRET_ACCESS_KEY)
    bucket="solidmedicaltest"
    res = oss.create_bucket(bucket,"public-read")
    hashCode=hashlib.md5(str(diagnoseId)).hexdigest().lower()
    ossFileName='%i_%s'%(diagnoseId,hashCode)
    #res = oss.upload_large_file(bucket, ossFileName, fileName)
    res2=oss.put_object_from_file(bucket,ossFileName,fileName)
    #info=oss.get_object_to_file(bucket,ossFileName,fileName)

    #oss.
    if (res2.status / 100) == 2:
        fileUrl='http://%s.%s/%s'%(bucket,WEB_HOST,ossFileName)
        return fileUrl
def listObjects():
    oss = OssAPI(HOST, ACCESS_ID, SECRET_ACCESS_KEY)
    bucket="solidmedicaltest"
    prefix = "1_c4ca4238a0b923820dcc509a6f75849b"
    marker = ""
    delimiter = "/"
    maxkeys = "100"
    headers = {}
    res = oss.get_bucket(bucket, prefix, marker, delimiter, maxkeys, headers)
    if (res.status / 100) == 2:
        body = res.read()
        h = GetBucketXml(body)
        (file_list, common_list) = h.list()
        print "object list is:"
        for i in file_list:
            print i
        print "common list is:"
        for i in common_list:
            print i
            obj=oss.get_object(bucket,i)
            print obj.msg
            print obj.read()





if __name__ == "__main__":
    # import  constant
    #
    # uploadFile(1,constant.DirConstant.DIAGNOSE_PDF_DIR+'test.pdf')
    listObjects()
# #初始化
#     if len(ACCESS_ID) == 0 or len(SECRET_ACCESS_KEY) == 0:
#         print "Please make sure ACCESS_ID and SECRET_ACCESS_KEY are correct in ", __file__ , ", init are empty!"
#         exit(0)
#     oss = OssAPI(HOST, ACCESS_ID, SECRET_ACCESS_KEY)
#
#     res = oss.create_bucket("solidmedicaltest","private")
#     print "%s\n%s" % (res.status, res.read())
#     sep = "=============================="
#
#     #对特定的URL签名，默认URL过期时间为60秒
#     method = "GET"
#     bucket = "solidmedicaltest" #+ time.strftime("%Y-%b-%d%H-%M-%S").lower()
#     object = "test_object"
#     url = "http://" + HOST + "/oss/" + bucket + "/" + object
#     headers = {}
#     resource = "/" + bucket + "/" + object
#
#     timeout = 60
#     url_with_auth = oss.sign_url_auth_with_expire_time(method, url, headers, resource, timeout)
#     print "after signature url is: ", url_with_auth
#     print sep
#     #创建属于自己的bucket
#     acl = 'private'
#     headers = {}
#     res = oss.put_bucket(bucket, acl, headers)
#     if (res.status / 100) == 2:
#         print "put bucket ", bucket, "OK"
#     else:
#         print "put bucket ", bucket, "ERROR"
#     print sep
#
#     #列出创建的bucket
#     res = oss.get_service()
#     if (res.status / 100) == 2:
#         body = res.read()
#         h = GetServiceXml(body)
#         print "bucket list size is: ", len(h.list())
#         print "bucket list is: "
#         for i in h.list():
#             print i
#     else:
#         print res.status
#     print sep
#
#     #把指定的字符串内容上传到bucket中,在bucket中的文件名叫object。
#     object = "object_test"
#     input_content = "hello, OSS"
#     content_type = "text/HTML"
#     headers = {}
#     res = oss.put_object_from_string(bucket, object, input_content, content_type, headers)
#     if (res.status / 100) == 2:
#         print "put_object_from_string OK"
#     else:
#         print "put_object_from_string ERROR"
#         print res.msg
#
#     print sep

