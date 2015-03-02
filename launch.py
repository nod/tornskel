#!/usr/bin/env python
import tornado.httpserver
import tornado.ioloop
import tornado.web
import sys

import app  # our application
from settings import app_settings

from optparse import OptionParser
from app.views.viewlib import route


def start_instance(settings):
    http_server = tornado.httpserver.HTTPServer(
        app.setup_app(settings)
        )
    http_server.listen(settings['port'])

    try: tornado.ioloop.IOLoop.instance().start()
    except KeyboardInterrupt: pass


def list_routes(routes):
        for r in routes:
            print '{:20s} => {}'.format(r.regex.pattern, r.name)


if __name__ == "__main__":
    parser = OptionParser()
    parser.add_option("-r", "--routes", action="store_true",
            help="print list of routes and exit" )
    parser.add_option("-p", "--port", help="specify httpd port")
    parser.add_option("-d", "--debug", action="store_true",
                      help="start with debugging enabled" )

    (options, args) = parser.parse_args()

    if options.routes:
        list_routes(route.get_routes())
        raise SystemExit

    if options.port:
        try: app_settings['port'] = int(options.port)
        except: pass
    elif args:
        try: app_settings['port'] = int(args[0])
        except: pass

    if options.debug:
        app_settings['debug'] = True

    print "starting Tornado{} on port {}".format(
        '(dbg)' if app_settings.get('debug') else '', app_settings['port'] )
    start_instance(app_settings)

