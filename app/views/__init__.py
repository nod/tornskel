
from viewlib import route, BaseHandler


@route('/')
class IndexHandler(BaseHandler):
    def get(self):
        self.render('index.html')


# this needs to be the last line after all views are defined
routes = route.get_routes()
