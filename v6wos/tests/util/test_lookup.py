import unittest.mock
import dns.exception
import v6wos.tests
import v6wos.util.lookup


class LookupTest(v6wos.tests.TestCase):

    @unittest.mock.patch("dns.resolver.Resolver")
    def test_check_aaaa(self, Resolver):
        Resolver.return_value = resolver = unittest.mock.Mock()
        resolver.query.return_value = [
            unittest.mock.Mock(address=b"2606:2800:220:1:248:1893:25c8:1946"),
        ]
        self.assertEqual(
            v6wos.util.lookup.check_aaaa("example.com"),
            ["2606:2800:220:1:248:1893:25c8:1946"])
        resolver.query.side_effect = dns.exception.UnexpectedEnd()
        self.assertEqual(v6wos.util.lookup.check_aaaa("example.com"), [])

    @unittest.mock.patch("dns.resolver.Resolver")
    def test_check_aaaa_nameservers(self, Resolver):
        Resolver.return_value = resolver = unittest.mock.Mock()
        resolver.query.return_value = [
            unittest.mock.Mock(address=b"2606:2800:220:1:248:1893:25c8:1946"),
        ]
        self.assertEqual(
            v6wos.util.lookup.check_aaaa("example.com", ["8.8.8.8"]),
            ["2606:2800:220:1:248:1893:25c8:1946"])
        self.assertEqual(resolver.nameservers, ["8.8.8.8"])
