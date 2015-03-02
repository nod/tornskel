from os import path

import tornado.httpserver
import tornado.ioloop
import tornado.web

import views

def setup_app(settings):
    # intialize our tornado instance
    app = tornado.web.Application(views.routes, **settings)
    return app
