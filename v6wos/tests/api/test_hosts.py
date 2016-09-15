import unittest.mock
import v6wos.tests
import v6wos.tests.api


class HostsHandlerTest(v6wos.tests.api.TestCase):

    @unittest.mock.patch("v6wos.model.hosts.Hosts")
    def test_get(self, Hosts):
        model = Hosts.return_value
        model.get.return_value = v6wos.tests.future([
            {
                "aaaa": [
                    "2606:2800:220:1:248:1893:25c8:1946",
                ],
                "name": "example.com",
            },
        ])
        res = self.fetch("/api/hosts")
        self.assertEqual(res.code, 200)
        self.assertEqual(res.json, {
            "hosts": [
                {
                    "aaaa": [
                        "2606:2800:220:1:248:1893:25c8:1946",
                    ],
                    "name": "example.com",
                },
            ],
        })
        model.all_hosts = ["google.com"]
        model.put.return_value = v6wos.tests.future({
            "aaaa": [
                "2a00:1450:4001:817::200e",
            ],
            "name": "google.com",
        })
        res = self.fetch("/api/hosts/example.com")
        self.assertEqual(res.code, 404)
        res = self.fetch("/api/hosts/google.com")
        self.assertEqual(res.code, 200)
        self.assertEqual(res.json, {
            "aaaa": [
                "2a00:1450:4001:817::200e",
            ],
            "name": "google.com",
        })
