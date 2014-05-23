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

    def test_addConsult(self):
        rv = self.app.post('/consult/add', data=dict(
            userId=1,
            doctorId=1,
            title='咨询一下关于颈部问题的',
            content='咨询一下关于颈部问题的解决方案'
        ), follow_redirects=True)


if __name__ == '__main__':
    unittest.main()
