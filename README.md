
tornskel
========

      _________
      \_______
        _____/    tornskel - Tornado Skeleton
        \___      fully functional skeletal template app for a tornado web app
          _/
          \


LICENSE
-------

This falls under the same license as TornadoWeb,
the Apache License, Version 2.0
Get a copy at http://www.apache.org/licenses/LICENSE-2.0.html

GETTING STARTED
---------------

You'll need to create a `settings_dev.py` or `settings_prod.py` in order to run
tornskel.  The easiest way to do this is to copy settings_dev.py.template to
settings_dev.py.

    cp settings_dev.py.template settings_dev.py

Once you have your local settings created, check out the options to launch.py
as follows.

	./launch.py -h
	Usage: launch.py [options]

	Options:
	  -h, --help            show this help message and exit
	  -r, --routes          print list of routes
	  -p PORT, --port=PORT  specify httpd port

If you just execute `./launch.py`, a Tornado instance will be running at the
port specified under port in settings.py or settings_dev.py if you
edited that.

Additional Notes
================

Tornskel adds a few helpers beyond the standard Tornado instance, but all of
these live in user space and can exist in your standard project library with no
patching of Tornado needed.

Handler Routing
---------------

Tornado's default way of routing URLs to handlers is by passing a large
list to the tornado app instance when it's created.  This is ok if you have a
few handlers, but can get a little unwieldy after a while.  Also, it just feels
odd to us to have to add a handler in one place, then go elsewhere to actually
activate the handler.

To ease that, tornskel offers a `@route(..)` decorator for handlers.  If your
handlers extend tornskel.views.viewlib.BaseHandler, you can use this route
decorator anytime you create a handler.

An example below will make this clear.

    @route('/some/path')
    class SomeRequestHandler(RequestHandler):
        pass

Then, when instantiating your tornado app, you can just pass in
route.get_routes() where tornado wants the url routes and it will provide the
urls and handlers list that tornado expects.  In tornskel, we generate this
route list as a member of the tornskel.tornapp.views module called `routes`.
In tornskel/tornapp/app.py, we hand this member to our
`tornado.web.Application(..)` instantiation call, just like you would with any
other tornado app.  The difference is that our routes are built at startup
dynamically instead of being defined statically.

You can see this list at any time by running `launch.py` with the `--routes`
option.

    ./launch.py --routes
        /      => tornapp.views.IndexHandler
        /yield => tornapp.views.YieldExampleHandler

*Note:* The order of routes appearing here is very important, as the first one
encountered that matches will be the one that tornado uses.  For this reason,
when you import the views into your project is how you affect this list.

If you don't want to use the `@route(...)` decorator, just write your views and
app in the standard tornado way and pretend the decorator doesn't exist.
Everything will still work just fine.

Yielded Asynchronous Calls
--------------------------

Part of the reason that tornado is so fast is that performing asynchronous
calls is very easy to incorporate with tornado's ioloop.  Unfortunately, this
can lead to a leapfrog approach to your handlers.  Typically, you call
asynchronously, and give it a function pointer to a callback.  This means
you need to save the state of the existing function somewhere, usually `self`,
and then pick that back up again in the callback function.  Performing
iterations with multiple callbacks can be a bit tricky as you end up hopping
between callbacks.  We have a solution for this.

If you decorate a request handler method with `@async_yield`, when you make an
async call, you can use python's `yield` to _yield execution_ to that call
until it returns.  This is a bit of a break from the standard way of thinking
about python's `yield`, but seems to work quite well.  You get the ease of
developing typical, serial, blocking code, but with the speed of async calls.

An example should help.

    class MyHandler(BaseHandler):
        @async_yield
        def get(self):
            ... stuff ...
            yield AsyncHTTPClient().fetch(
                'http://example.com/',
                callback=self.yield_cb  # always use this
                )
            print "stuff returned is in", results

You can use tornskel without this feature, it's just there if you'd like
it.  To read more on this, see the source for tornskel/tornapp/views/viewlib.py
and pay close attention to the comments in `async_yield(...)`.

