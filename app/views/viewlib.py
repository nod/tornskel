
import tornado.web
from tornado.escape import json_encode


class BaseHandler(tornado.web.RequestHandler):

    def get_current_user(self):
        user = self.get_secure_cookie("authed_user")
        return user or None

    def _api_out(self, ok, data=None, msg=None):
        return self.write(json_encode(dict(ok=ok, data=data, msg=msg)))

    def api_ok(self, data=None, msg=None):
        return self._api_out(True, data=data, msg=msg)

    def api_fail(self, msg=None):
        return self._api_out(False, msg=msg)


