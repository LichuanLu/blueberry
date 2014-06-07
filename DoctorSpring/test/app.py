# coding: utf-8

__author__ = 'chengc017'
import os
import unittest
from DoctorSpring import app

import tempfile

class FlaskrTestCase(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
    def test_messages(self):
        #self.login('admin', 'default')

        rv = self.app.post('/addDiagnoseComment.json', form=dict(
            userId=1,
            receiverId=1,
            diagnoseId=1,
            content='诊断很不错，非常感谢'
        ), follow_redirects=True)
        assert 'No entries here so far' not in rv.data
        assert '&lt;Hello&gt;' in rv.data
        assert '<strong>HTML</strong> allowed here' in rv.data
    def test_commentList(self):
        #self.login('admin', 'default')

        rs = self.app.get('/observer/1/diagnoseCommentList.json',follow_redirects=True)
        print rs

    def test_getDiagnosesByAdmin(self):
        #self.login('admin', 'default')

        rs = self.app.get('/admin/diagnose/list/all?hostpitalId=1,3&doctorName=任志强',follow_redirects=True)
        print rs

    def test_getDiagnosePostionList(self):
        #self.login('admin', 'default')

        rs = self.app.get('/diagnoseTemplate/diagnoseAndImageDesc?diagnoseMethod=ct&diagnosePostion=内 分 泌',follow_redirects=True)


    def test_addConsult(self):
        rv = self.app.post('/consult/add', data=dict(
            userId=1,
            doctorId=1,
            title='咨询一下关于颈部问题的',
            content='咨询一下关于颈部问题的解决方案'
        ), follow_redirects=True)
    def test_addThanksNote(self):
        rv = self.app.post('/gratitude/create', data=dict(
            receiver=4,
            content='这是我得一封感谢信，非常感谢医生对我的医治'
        ), follow_redirects=True)

    def test_addFavorties(self):
        rv = self.app.post('/userFavorties/add', data=dict(
            userId=1,
            doctorId=1,
            type=0,
        ), follow_redirects=True)
    def test_addReport(self):
        rv = self.app.post('/admin/report/addOrUpate', data=dict(
            status=2,
            reportId=1,
            diagnoseId=1,
            imageDesc='肺窗示右肺上叶尖段/后段/前段|中叶内侧段/外侧段|下叶前/外/后/内基底段/背段|左肺上叶尖后段/前段/舌段|下叶前外/后/内/基底段/背段/可见一孤立性肿块/结节影，大小约为　Ｘ　cm，边缘毛糙，可见分叶及细小毛刺，密度均匀/不均匀，CT值  Hu，其内可见偏心性空洞，肿块内无钙化/点状少量钙化，纵隔窗示纵隔内可见多个肿大淋巴结。左/右侧胸腔内可见弧形低密度影，心影及大血管形态正常。     ',
            diagnoseDesc='1.左/右肺上叶/中叶/下叶占位性病变，考虑为周围型肺癌并肺门及纵隔淋巴结转移。2.左/右侧胸腔积液。 CHANGE',
            ), follow_redirects=True)
        print rv





if __name__ == '__main__':
    unittest.main()
