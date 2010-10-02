
from viewlib import route, BaseHandler, async_yield


@route('/')
class IndexHandler(BaseHandler):
    def get(self):
        self.render('index.html')


@route('/yield')
class YieldExampleHandler(BaseHandler):
    """
    This is a simple example showing how to use the inline async call.
    """

    @async_yield
    def get(self):
        from tornado.httpclient import AsyncHTTPClient
        from tornado.escape import json_decode
        uri = "http://search.twitter.com/search.json?q=bcstx"
        yield AsyncHTTPClient().fetch(uri, self.yield_cb)
        if not self._yielded:
            self.render('fail.html')
            return
        print self._yielded
        tweets = json_decode(self._yielded[0].body)['results']
        self.render('yield_example.html', tweets=tweets)

# this needs to be the last line after all views are instantiated
routes = route.get_routes()
