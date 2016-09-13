import unittest.mock
import v6wos.tests
import v6wos.util.cache


class HostsCacheTest(v6wos.tests.TestCase):

    @unittest.mock.patch("v6wos.util.lookup.check_aaaa")
    @unittest.mock.patch("v6wos.util.cache.HostsCache.get_hosts")
    def test_warmup(self, get_hosts, check_aaaa):
        get_hosts.return_value = ["example.com"]
        check_aaaa.return_value = ["2606:2800:220:1:248:1893:25c8:1946"]
        hosts_cache = v6wos.util.cache.HostsCache()
        hosts_cache.warmup(nameservers=["0.0.0.0"])
        self.assertEqual(hosts_cache, {
            "example.com": {
                "host": "example.com",
                "aaaa": [
                    "2606:2800:220:1:248:1893:25c8:1946",
                ],
            },
        })
        check_aaaa.assert_called_once_with(
            "example.com", nameservers=["0.0.0.0"])
