import unittest.mock
import json
import copy
import pkg_resources
import yaml
import tornado.testing
import c24


class TestCase(tornado.testing.AsyncHTTPTestCase,
               tornado.testing.LogTrapTestCase):

    config = c24.Application.default_config

    @unittest.mock.patch("c24.Application.load_config")
    def get_app(self, load_config):
        load_config.return_value = copy.deepcopy(self.config)
        self.application = c24.Application(config=None, debug=True)
        return self.application

    def fetch(self, *args, **kwargs):
        if "headers" not in kwargs:
            kwargs["headers"] = {}
        if "body" in kwargs and isinstance(kwargs["body"], dict):
            kwargs["body"] = json.dumps(kwargs["body"]).encode()
            kwargs["headers"]["Content-Type"] = "application/json"
        response = super().fetch(*args, **kwargs)
        return response


class DistributionTest(TestCase):

    dist = pkg_resources.get_distribution(__package__.split(".")[0])

    def test_version(self):
        self.assertEqual(self.dist.version, c24.__version__)
        self.assertRegex(c24.__version__, r"\d+\.\d+\.\d+")


class ApplicationTest(TestCase):

    @unittest.mock.patch("os.path.exists")
    def test_read_config(self, exists):
        exists.return_value = True
        read_data = yaml.dump(self.config)
        mock_open = unittest.mock.mock_open(read_data=read_data)
        with unittest.mock.patch('builtins.open', mock_open, create=False):
            config = self.application.load_config("config.yaml")
        self.assertEqual(config, self.config)
        exists.return_value = False
        mock_open = unittest.mock.mock_open(read_data=read_data)
        with unittest.mock.patch('builtins.open', mock_open, create=True):
            config = self.application.load_config("config.yaml")
        self.assertEqual(config, self.config)


class HTTPServerTest(TestCase):

    @unittest.mock.patch("tornado.httpserver.HTTPServer.bind")
    def test_bind(self, bind):
        server = c24.HTTPServer(self.application)
        server.bind()
        bind.assert_called_once_with(
            self.application.config["bind"]["port"],
            address=self.application.config["bind"]["addr"],
            backlog=self.application.config["http"]["tcp-backlog"])

    @unittest.mock.patch("c24.HTTPServer.bind")
    @unittest.mock.patch("c24.HTTPServer.add_sockets")
    def test_run(self, add_socket, bind):
        server = c24.HTTPServer(self.application)
        socket = unittest.mock.Mock()
        bind.side_effect = lambda: server._pending_sockets.append(socket)
        io_loop = unittest.mock.MagicMock()
        server.run(io_loop=io_loop)
        bind.assert_called_once_with()
        io_loop.start.assert_called_once_with()
        add_socket.assert_called_once_with([socket])


class TestHandler(c24.RequestHandler):

    def get(self):
        if self.request.headers.get("X-Response-Body"):
            self.write(self.request.headers["X-Response-Body"])
        else:
            self.set_status(204)

    def patch(self):
        raise tornado.web.HTTPError(405)

    def check_xsrf_cookie(self):
        pass


class TestApplication(c24.Application):

    handlers = [
        (r".*", TestHandler),
    ]


class HandlerTest(TestCase):

    @unittest.mock.patch("c24.Application.load_config")
    def get_app(self, load_config):
        load_config.return_value = self.config
        self.application = TestApplication(config=None, debug=True)
        return self.application

    def test_headers(self):
        res = self.fetch("/test")
        self.assertEqual(res.code, 204)
        res = self.fetch("/test", headers={"X-Response-Body": "1"})
        self.assertEqual(res.code, 200)
        self.assertEqual(res.body, b"1")

    def test_remove_slash(self):
        res = self.fetch("/test/", follow_redirects=False)
        self.assertEqual(res.code, 301)
        res = self.fetch("/test/", method="PATCH", body=b"")
        self.assertEqual(res.code, 405)
