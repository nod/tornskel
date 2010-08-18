#!/usr/bin/env python
import unittest, json, time
from threading import Thread, Semaphore
import sys, os
import urllib, urllib2, cookielib, urlparse

from tornado.httpserver import HTTPServer
from tornado.web import RequestHandler
from tornado.ioloop import IOLoop

from couchdbkit import Document

sys.path.insert(0,os.path.join(os.path.dirname(__file__), ".."))
import settings
import tornapp


__test__ = False


class TornTestCase(unittest.TestCase):

    def setUp(self):
        cj = cookielib.CookieJar()
        self.opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
        self.baseurl = 'http://localhost:%d'%settings.test_httpd_port

    def open(self, url, **kwargs):
        url = urlparse.urljoin(self.baseurl,url)
        if len(kwargs): #POST
            return self.opener.open(url,urllib.urlencode(kwargs))
        else: #GET
            return self.opener.open(url)

    def open_as_json(self, url, **kwargs):
        resp = self.open(url, **kwargs)
        out = resp.read()
        resp.close()
        return json.loads(out)


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


def main():
    def _fake_render(handler, template_name, **kwargs):
        handler.write(json.dumps(kwargs))
        handler.finish()
    RequestHandler.render = _fake_render
    
    thread = DebugServerThread(tornapp.setup_app(settings))
    thread.start()
    if settings.db_user:
        Document.get_db().flush()
    thread.loaded.acquire()
    try:
        unittest.main()
    finally:
        thread.stop()

if __name__ == '__main__':
    print "This file is not a test, and should not be run!"