#!/usr/bin/env python
import unittest, json, time
from threading import Thread, Semaphore
import sys, os

from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop

from restkit import Resource,RequestFailed
from couchdbkit import Document

sys.path.insert(0,os.path.join(os.path.dirname(__file__), ".."))
import settings
import tornapp  # our application


class TestViews(unittest.TestCase):

    def setUp(self):
        self.res = Resource('http://localhost:%d'%settings.test_httpd_port)

    def tearDown(self):
        pass

    def _get_as_json(self, url, **params):
        return json.loads(self.res.get(url, **params).body_string())

    def _post_to_json(self, url, **params):
        try:
            return json.loads(self.res.post(url, **params).body_string())
        except RequestFailed,e:
            return json.loads(e._get_message())

    def test_connect(self):
        resp = self.res.get('/')
        self.failUnlessEqual(200, resp.status_int)
        self.failUnless(len(resp.body_string())>0)


class DebugServerThread(Thread):
    def __init__(self, app):
        Thread.__init__(self)
        self.app = app
        self.daemon = True
        self.loaded = Semaphore(0)

    def run(self):
        self.http_server = HTTPServer(self.app)
        self.http_server.listen(settings.test_httpd_port)
        self.loaded.release()
        IOLoop.instance().start()

    def stop(self):
        self.http_server.io_loop.remove_handler(
                self.http_server._socket.fileno())
        self.http_server._socket.close()


if __name__ == '__main__':
    thread = DebugServerThread(tornapp.setup_app(settings))
    thread.start()
    if settings.db_user:
        Document.get_db().flush()
    thread.loaded.acquire()
    try:
        unittest.main()
    finally:
        thread.stop()
