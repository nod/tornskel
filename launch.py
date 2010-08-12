#!/usr/bin/env python
import tornado.httpserver
import tornado.ioloop
import tornado.web
import sys

import tornapp  # our application
import settings

def start_instance(settings):
    http_server = tornado.httpserver.HTTPServer(
        tornapp.setup_app(settings)
        )
    http_server.listen(settings.httpd_port)

    try: tornado.ioloop.IOLoop.instance().start()
    except KeyboardInterrupt: pass


if __name__ == "__main__":
    try: settings.httpd_port = int(sys.argv[1])
    except: pass
    start_instance(settings)
