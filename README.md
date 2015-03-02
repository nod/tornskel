
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

You'll need to edit `settings_local/__init__.py`.

Once you have your local settings created, check out the options to launch.py
as follows.

	./launch.py -h
	Usage: launch.py [options]

	Options:
	  -h, --help            show this help message and exit
	  -r, --routes          print list of routes
	  -p PORT, --port=PORT  specify httpd port

If you just execute `./launch.py`, a Tornado instance will be running at the
port specified under port in your settings.

Additional Notes
================

Tornskel adds a few helpers beyond the standard Tornado instance, but all of
these live in user space and can exist in your standard project library with no
patching of Tornado needed.

Handler Routing
---------------

Tornskel apps use [tornroutes](/nod/tornroutes) for handling setting up routes
to handlers.  You can use the standard routes list by modifying `launch.py`.

Here's an example of using tornroutes.

```python
@route('/some/path')
class SomeRequestHandler(RequestHandler):
  pass
```

You can see this list at any time by running `launch.py` with the `--routes`
option.

```bash
$ ./launch.py --routes
  /      => tornapp.views.IndexHandler
```

*Note:* The order of routes appearing here is very important, as the first one
encountered that matches will be the one that tornado uses.  For this reason,
when you import the views into your project is how you affect this list.  I'm not typically a fan of compile time side effects, but ... eh.

If you don't want to use the `@route(...)` decorator, just write your views and
app in the standard tornado way and pretend the decorator doesn't exist.
Everything will still work just fine.

