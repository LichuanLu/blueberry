#coding=utf8
import time

from oss.oss_api import *
from DoctorSpring.models import Diagnose
from DoctorSpring.util import constant
from oss.oss_xml_handler import *
from oss.oss_util import *
import mimetypes
import  hashlib
__author__ = 'chengc017'


HOST = "oss.aliyuncs.com"
WEB_HOST="oss-cn-hangzhou.aliyuncs.com"
ACCESS_ID = "5XxlKb2HfhZWlyLY"
SECRET_ACCESS_KEY = "SuqEzwOL5Pcl8VZZMgl0cPsgQqboDh"
bucket="solidmedicaltest"
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
def copyObjects():
    oss = OssAPI(HOST, ACCESS_ID, SECRET_ACCESS_KEY)
    bucket="solidmedicaltest"
    prefix = "1_c4ca4238a0b923820dcc509a6f75849b/"
    marker = ""
    delimiter = "/"
    maxkeys = "100"
    headers = {}
    res = oss.get_bucket(bucket, prefix, marker, delimiter, maxkeys, headers)
    if (res.status / 100) == 2:
        body = res.read()
        print body
        h = GetBucketXml(body)
        (file_list, common_list) = h.list()
        print "object list is:"
        for i in file_list:
            fileName= i[0]
            diagnoseId=getDiagnoseIdFromFileName(fileName)
            diagnose=Diagnose.getDiagnoseByDiagnoseSeriesNo(diagnoseId)
            if diagnose:
                oss.copy_object(bucket,i,bucket,diagnoseId)
                fileName=constant.DirConstant.DIAGNOSE_PDF_DIR+'temp.pdf'
                rs=oss.get_object_to_file(bucket,i,fileName,None)
                print rs.msg





        # print "common list is:"
        # for i in common_list:
        #     print i
        #
        #     index=i.__len__()-1
        #     i=i[:index]
        #
        #
        #     obj=oss.get_object(bucket,i)
        #     print obj.msg
        #     print obj.read()

def getDiagnoseIdFromFileName(fileName):
    if fileName and fileName.find('/')>-1:
        fileNames=fileName.split('/')
        fileName=fileNames[1]
        if fileName and fileName.find('.')>0:
            fileNames=fileName.split('.')
            diagnoeId=fileNames[0]
            return diagnoeId

def uploadFileFromString(diagnoseId,fileName,input_content,content_type,headers):
    if len(ACCESS_ID) == 0 or len(SECRET_ACCESS_KEY) == 0:
        print "Please make sure ACCESS_ID and SECRET_ACCESS_KEY are correct in ", __file__ , ", init are empty!"
        exit(0)
    oss = OssAPI(HOST, ACCESS_ID, SECRET_ACCESS_KEY)
    bucket="solidmedicaltest"
    res = oss.create_bucket(bucket,"public-read")
    hashCode=hashlib.md5(str(diagnoseId)).hexdigest().lower()
    ossFileName='%i_%s'%(diagnoseId,hashCode)
    #res = oss.upload_large_file(bucket, ossFileName, fileName)
    # res2=oss.put_object_from_file(bucket,ossFileName,fileName)
    #info=oss.get_object_to_file(bucket,ossFileName,fileName)
    res2 = oss.put_object_from_fp(bucket, ossFileName, input_content, content_type, headers)


    #oss.
    if (res2.status / 100) == 2:
        fileUrl='http://%s.%s/%s'%(bucket,WEB_HOST,ossFileName)
        return fileUrl

def get_connection():

    return OssAPI(HOST, ACCESS_ID, SECRET_ACCESS_KEY)

def _put_file( filename, content):
    content_type = mimetypes.guess_type(filename)[0] or "application/x-octet-stream"
    result = get_connection().put_object_from_string(bucket, filename, content, content_type)
    if result.status / 100 == 2:
        return True
    else:
        raise IOError("OSSStorageError: %s" % result.read())
def _clean_name( name):
    return os.path.normpath(name).replace("\\", '/')

def _save( name, content):
    name = _clean_name(name)
    _put_file(name, content)
    return name

# def _open( name, mode='rb'):
#     name = _clean_name(name)
#     f = AliyunOssFile(name, 'rb', self)
#     if not f.key:
#         raise IOError('')
#     return f

def _read( name):
    name = _clean_name(name)
    res = get_connection().get_object(bucket, name)
    if (res.status / 100) == 2:
        return res.read()
    else:
        raise IOError("OSSStorageReadError: %s", res.read())

def delete( name):
    name = _clean_name(name)
    res = get_connection().delete_object(bucket, name)
    if res.status != 204:
        raise IOError("OSSStorageError: %s" % res.read())
    else:
        return True

def exists( name):
    name = _clean_name(name)
    res = get_connection().head_object(bucket, name)
    return (res.status / 100) == 2

def listdir( path):
    path = _clean_name(path)
    res = get_connection().get_object_group_index(bucket, path)
    if (res.status / 100) == 2:
        print "get_object_group_index OK"
        body = res.read()
        h = GetObjectGroupIndexXml(body)
        for i in h.list():
            print "object group part msg:", i
        else:
            print "get_object_group_index ERROR"
    return

def size( name):
    name = _clean_name(name)
    res = get_connection().head_object(bucket, name)
    header_map = convert_header2map(res.getheaders())
    content_length = safe_get_element("content-length", header_map)
    return content_length and int(content_length) or 0


if __name__ == "__main__":
    # import  constant
    #
    # uploadFile(1,constant.DirConstant.DIAGNOSE_PDF_DIR+'test.pdf')
    copyObjects()
    #listdir('/1_c4ca4238a0b923820dcc509a6f75849b/')
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

