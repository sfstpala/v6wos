import unittest.mock
import pkg_resources
import v6wos
import v6wos.tests.api


class HostsHandlerTest(v6wos.tests.api.TestCase):

    def test_get(self):
        with open(pkg_resources.resource_filename(
                "v6wos", "resources/top100.txt")) as f:
            hosts = [i.strip() for i in f.readlines() if i.strip()]
        res = self.fetch("/api/hosts")
        self.assertEqual(res.code, 200)
        self.assertEqual(res.json, {"hosts": hosts})


class HostsDetailHandlerTest(v6wos.tests.api.TestCase):

    @unittest.mock.patch("v6wos.util.lookup.check_aaaa")
    def test_get(self, check_aaaa):
        check_aaaa.return_value = ["2a00:1450:4001:810::200e"]
        res = self.fetch("/api/hosts/google.com")
        self.assertEqual(res.code, 200)
        self.assertEqual(res.json, {
            "aaaa": [
                "2a00:1450:4001:810::200e",
            ],
            "host": "google.com",
        })

    @unittest.mock.patch("v6wos.util.lookup.check_aaaa")
    def test_get_not_found(self, check_aaaa):
        check_aaaa.return_value = ["2606:2800:220:1:248:1893:25c8:1946"]
        res = self.fetch("/api/hosts/example.com")
        self.assertEqual(res.code, 404)
