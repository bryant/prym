from werkzeug import Request
from werkzeug.exceptions import HTTPException
from werkzeug.routing import Map, Rule

class route(object):
    attr_stamp = "_routes"

    def __init__(self, path, **kwargs):
        self.path = path
        self.kwargs = kwargs

    def __call__(self, fn):
        stamps = getattr(fn, self.attr_stamp, set())
        endpoint = urlify(fn.__name__)

        z = (self.path, tuple(self.kwargs.items()))
        stamps.add(z)
        setattr(fn, self.attr_stamp, stamps)

        return fn

def urlify(name):
    return name.replace("_", "-").lower()

# todo: rename app
class PrymApp(object):
    def __init__(self):
        self.views = {}
        self.routes = Map()

    def add_url(self, url, fn, **kwargs):
        endpoint = kwargs.get("endpoint", urlify(fn.__name__))
        kwargs["endpoint"] = endpoint

        if endpoint in self.views:
            print "w: overwriting endpoint [%s] bound to [%s]" % \
                  (endpoint, self.views[endpoint])

        self.views[endpoint] = fn
        self.routes.add(Rule(url, **kwargs))
        return self

    def scan_for_routes(self, namespace):
        for entry in namespace.__dict__.values():
            routes = getattr(entry, route.attr_stamp, None)

            if routes is None:
                continue

            for url, kwargs in routes:
                self.add_url(url, entry, **dict(kwargs))

        return self

    def make_response(self, rv):
        if not isinstance(rv, Response):

            if isinstance(rv, basestring):
                rv = Response(rv)
            elif isinstance(rv, tuple):
                rv = Response(*rv)
            else:
                rv = Response(str(rv))

        return rv

    def wsgi_app(self, environ, start_response):
        adapter = self.routes.bind_to_environ(environ)

        try:
            endpoint, args = adapter.match()
        except HTTPException as e:
            rv = e
        else:
            req = Request(environ)
            req.view_args = args
            rv = self.make_response(self.views[endpoint](req))

        return rv(environ, start_response)

    def __call__(self, environ, start_response):
        return self.wsgi_app(environ, response)

    def serve(self, host, port):
        from wsgiref.simple_server import make_server
        print "Serving on 0.0.0.0:8000"
        make_server(host, port, self).serve_forever()
