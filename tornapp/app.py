from os import path

import tornado.httpserver
import tornado.ioloop
import tornado.web

from couchdbkit import  Document
from couchdbkit.client import Server
from couchdbkit.loaders import FileSystemDocsLoader

import views

def setup_app(settings):
    # intialize our tornado instance
    app = tornado.web.Application([
        (r"/", views.IndexHandler),
        (r"/signup", views.SignupHandler),
        (r"/signup/complete", views.SignupCompleteHandler),
        ], **settings)

    # couchdb setup
    if settings['db_user']:
        from restkit import BasicAuth
        server = Server(
            uri=settings['db_uri'],
            filters=[
                BasicAuth(settings['db_user'], settings['db_pass'])
                ],
            )
        db = server.get_or_create_db(settings['db_name'])
        # now attach our couchdb instance to the tornado app instance
        app.couchdb = db

        # setup couchdb views
        loader = FileSystemDocsLoader(path.join(
            path.dirname(__file__),
            '_design'
            ) )
        loader.sync(db, verbose=True)

    return app
