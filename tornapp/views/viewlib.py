
import tornado.web
from tornado.escape import json_encode, json_decode


class BaseHandler(tornado.web.RequestHandler):

    def get_current_user(self):
        user = self.get_secure_cookie("authed_user")
        return user or None

    def ok(self, data=None):
        self.write(json_encode({'status':'ok', 'data':data}))

    def fail(self, reason=None):
        self.write(json_decode({'status':'fail', 'reason': reason}))

    def yield_cb(self, *args, **ka):
        """
        generic callback that enables the yield async syntax
        """
        self._yielded = args
        self._yielded_kwargs = ka
        try: self._yield_iter.next()
        except StopIteration: pass

    def _handle_request_exception(self, e):
        tornado.web.RequestHandler._handle_request_exception(self,e)
        import pdb
        pdb.post_mortem()


def async_yield(f):
    """
    Decorates request handler methods on an BaseRequestHandler object such
    that we can use the yield keyword for a bit of code cleanup to make it
    easier to write and use asynchronous calls w/o having to drop into the
    callback function to continue execution.  This makes execution much easier
    to handle as we don't have to attach all method state to self and also
    following the code execution now stays in the same method.

    USAGE
    =====

    class MyHandler(BaseHandler):
        @async_yield
        def get(self):
            ... stuff ...
            yield http_fetch(
                'http://blah',
                callback=self._yield_cb  # always use this
                )
            print "stuff returned is in", self._yielded


    TECH NOTES
    ==========

    This is hard coded to be used with AppBaseRequestHandler objects and
    actually just turns the get/post/etc methods into generators and we then
    take advantage of this nature and begin execution with a call to
    self._yield_iter.next() which actually begins execution of the method.
    Then, when yield is encountered with an asynchronous call, we halt
    execution of the method until the our generic callback, self._yield_cb, is
    reached where we save off the results in self._yielded and
    self._yielded_kwargs and then call self._yield_iter.next() again to pick up
    right after the asynchronous call.


    BUT WAIT
    ========

    Q: Doesn't the yield essentially halt the execution of the handler until
       the callback returns?
    A: YES. And, I'm ok with that.  This implementation is much more preferable
       than the series of hops we were doing and accomplishes the same thing in
       a much more elegant way.  And, if we need to do true async in multiple
       paths, there's always the original way.

    Q: What if I mix this yield stuff with the tornado async way of doing
       things like in the docs?
    A: Don't do it. Not. Cool. Dude.
    """
    f = tornado.web.asynchronous(f)
    def yielding_asynchronously(self, *a, **ka):
        self._yield_iter = f(self, *a, **ka)
        self._yield_iter.next()
    return yielding_asynchronously






def just_template(templ):
    """Generate a transient view dynamically to render straight to template."""
    class TransientGenericView(BaseHandler):
        def get(self): self.render(templ)
    return TransientGenericView


class route(object):
    """
    decorates RequestHandlers and builds up a list of routables handlers

    Tech Notes (or "What the *@# is really happening here?")
    --------------------------------------------------------

    Everytime @route('...') is called, we instantiate a new route object which
    saves off the passed in URI.  Then, since it's a decorator, the function is
    passed to the route.__call__ method as an argument.  We save a reference to
    that handler with our uri in our class level routes list then return that
    class to be instantiated as normal.

    Later, we can call the classmethod route.get_routes to return that list of
    tuples which can be handed directly to the tornado.web.Application
    instantiation.

    Example
    -------

    @route('/some/path')
    class SomeRequestHandler(RequestHandler):
        pass

    my_routes = route.get_routes()
    """
    _routes = []

    def __init__(self, uri):
        self._uri = uri

    def __call__(self, _handler):
        """gets called when we class decorate"""
        self._routes.append((self._uri, _handler))
        return _handler

    @classmethod
    def get_routes(self):
        return self._routes



