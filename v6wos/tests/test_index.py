import unittest.mock
import v6wos.tests


class IndexHandlerTest(v6wos.tests.TestCase):

    @unittest.mock.patch("v6wos.RequestHandler.fetch")
    def test_get(self, fetch):
        self.application.hosts_cache = {}
        fetch.side_effect = [
            v6wos.tests.future(unittest.mock.Mock(code=200, json={
                "hosts": ["example.com"],
            })),
            v6wos.tests.future(unittest.mock.Mock(code=200, json={
                "aaaa": [
                    "2606:2800:220:1:248:1893:25c8:1946",
                ],
                "host": "example.com",
            })),
            v6wos.tests.future(unittest.mock.Mock(code=200, json={
                "hosts": ["example.com"],
            })),
        ]
        res = self.fetch("/")
        self.assertEqual(res.code, 200)
        res = self.fetch("/")
        self.assertEqual(res.code, 200)

    @unittest.mock.patch("v6wos.RequestHandler.fetch")
    def test_get_service_unavailable(self, fetch):
        self.application.hosts_cache = {}
        fetch.side_effect = [
            v6wos.tests.future(unittest.mock.Mock(code=500)),
            v6wos.tests.future(unittest.mock.Mock(code=200, json={
                "hosts": ["example.com"],
            })),
            v6wos.tests.future(unittest.mock.Mock(code=500)),
        ]
        res = self.fetch("/")
        self.assertEqual(res.code, 503)
        res = self.fetch("/")
        self.assertEqual(res.code, 503)
