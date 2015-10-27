#!/usr/bin/env python
import unittest
import json
from threading import Thread, Semaphore
import urllib
import urllib2
import cookielib
import urlparse

from tornado.httpserver import HTTPServer
from tornado.web import RequestHandler
from tornado.ioloop import IOLoop
from couchdbkit import Document

__test__ = False


class TornTestCase(unittest.TestCase):

    def setUp(self, port):
        cj = cookielib.CookieJar()
        self.opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
        self.baseurl = 'http://localhost:%d'%port

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
        self.http_server.listen(self.app.settings['port'])
        self.loaded.release()
        IOLoop.instance().start()


def launch(app):
    def _fake_render(handler, template_name, **kwargs):
        handler.write(json.dumps(kwargs))
        handler.finish()
    RequestHandler.render = _fake_render
    
    thread = DebugServerThread(app)
    thread.start()
    if app.settings['db_user']:
        Document.get_db().flush()
    thread.loaded.acquire()

if __name__ == '__main__':
    print "This file is not a test, and should not be run!"
