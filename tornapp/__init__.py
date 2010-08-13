from app import setup_app

# first, check that the server admin has installed everything needed.
# TODO: check version numbers here.
import couchdbkit
import restkit
import tornado.web
