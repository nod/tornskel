#!/usr/bin/env python
import unittest, json, time
import sys, os

sys.path.insert(0,os.path.join(os.path.dirname(__file__), ".."))
from test_settings import torn_settings
import tornapp  # our application
import torn_test_case

class TestViews(torn_test_case.TornTestCase):

    def setUp(self):
        torn_test_case.TornTestCase.setUp(self, torn_settings['port'])

    def tearDown(self):
        pass

    def test_connect(self):
        resp = self.open('/')
        self.failUnlessEqual(200,resp.getcode())
        self.failUnless(len(resp.read())>0)

    def test_signup(self):
        email = 'noreply@collectivelabs.com'
        json = self.open_as_json('/signup', email=email)
        self.failUnlessEqual(json['signup'], email)


if __name__ == '__main__':
    torn_test_case.launch(tornapp.setup_app(torn_settings))
    unittest.main()
