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
    http_server.listen(settings['port'])

    try: tornado.ioloop.IOLoop.instance().start()
    except KeyboardInterrupt: pass


if __name__ == "__main__":
    parser = OptionParser()
    parser.add_option("-r", "--routes", action="store_true",
            help="print list of routes and exit")
    parser.add_option("-p", "--port", help="specify httpd port")
    (options, args) = parser.parse_args()

    if options.routes:
        routes = route.get_routes()
        L = max( len(r) for r,c in routes ) # len of longest path
        fmt_ = "    %%-%ds => %%s" % L
        for r,c in  routes:
            print fmt_ % (r, ".".join((c.__module__, c.__name__)))
        sys.exit(0)
    elif options.port:
        try: settings['port'] = int(options.port)
        except: pass
    elif args:
        try: settings['port'] = int(args[0])
        except: pass
    print "starting Tornado on port", settings['port']
    start_instance(settings)
