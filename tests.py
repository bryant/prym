from prym import route, PrymApp
from werkzeug.test import EnvironBuilder
import unittest

class FrameworkTest(unittest.TestCase):
    def test_route(self):
        @route("/multiple/")
        @route("/accessible/")
        @route("/routes/")
        def dummy():
            pass

        assert getattr(dummy, route.attr_stamp) == \
               set([("/multiple/", ()), ("/accessible/", ()),
                    ("/routes/", ())])

    def test_route_scaning(self):
        class namespace(object):
            @route("/routeA/")
            def route_a(request):
                pass

            def route_b(request):
                pass

        app = PrymApp()
        map_ = app.routes

        app.scan_for_routes(namespace)
        assert len(map_._rules) == 1
        assert "route-a" in app.views

        env = EnvironBuilder("/routeA/")
        assert map_.bind_to_environ(env.get_environ()).match() is not None

    def test_add_url(self):
        class namespace(object):
            def route_a(request):
                pass

            def route_b(request):
                pass

        app = PrymApp()
        map_ = app.routes

        app.add_url("/routeA/", namespace.route_a)
        assert len(map_._rules) == 1
        assert "route-a" in app.views

        env = EnvironBuilder("/routeA/")
        assert map_.bind_to_environ(env.get_environ()).match() is not None

if __name__ == "__main__":
    unittest.main()
