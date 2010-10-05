#!/usr/bin/env python
import tornado.httpserver
import tornado.ioloop
import tornado.web
import sys

import tornapp  # our application
from settings import torn_settings as settings

from optparse import OptionParser
from tornapp.views.viewlib import route

def start_instance(settings):
    http_server = tornado.httpserver.HTTPServer(
        tornapp.setup_app(settings)
        )
    http_server.listen(settings['httpd_port'])

    try: tornado.ioloop.IOLoop.instance().start()
    except KeyboardInterrupt: pass


if __name__ == "__main__":
    parser = OptionParser()
    parser.add_option("-r", "--routes", action="store_true",
            help="print list of routes")
    parser.add_option("-p", "--httpd-port", help="specify httpd port")
    (options, args) = parser.parse_args()

    if options.routes:
        for r,c in  route.get_routes():
            print "%s => %s" % (r,c.__name__)
        sys.exit(0)
    elif options.httpd_port:
        try: settings['httpd_port'] = int(options.httpd_port)
        except: pass
    elif args:
        try: settings['httpd_port'] = int(args[0])
        except: pass

    start_instance(settings)
