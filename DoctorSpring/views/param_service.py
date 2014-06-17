# coding: utf-8
__author__ = 'chengc017'
import string

class UserCenter(object):
    @staticmethod
    def getDiagnoseListByAdmin(hospitals):
        if hospitals is None:
            return
        if hospitals.find(',')!=-1:
            hospitalList= hospitals.split(',')
            return map(lambda x:string.atoi(x),hospitalList)

        else:
            result=[]
            result.append(string.atoi(hospitals))
            return result

if __name__ == '__main__':
    print UserCenter.getDiagnoseListByAdmin('1')



