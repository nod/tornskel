from os import path

# couchdb related
db_name = ""
db_uri  = ""
db_user = ""
db_pass = ""

# tornado specific
httpd_port = 6488
torn_settings = {
    "debug":True,
    "login_url": "/auth/login",
    "static_path": path.join(path.dirname(__file__), "tornapp/static"),
    "template_path": path.join(path.dirname(__file__), "tornapp/templates"),
    "cookie_secret": "SOMETHING HERE",
    }

