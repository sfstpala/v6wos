import unittest.mock
import dns.exception
import v6wos.tests
import v6wos.util.lookup


class LookupTest(v6wos.tests.TestCase):

    @unittest.mock.patch("dns.resolver.Resolver")
    def test_check_aaaa(self, Resolver):
        Resolver.return_value = resolver = unittest.mock.Mock()
        resolver.query.return_value = [
            unittest.mock.Mock(address="2606:2800:220:1:248:1893:25c8:1946"),
        ]
        self.assertEqual(
            v6wos.util.lookup.check_aaaa("example.com", ["8.8.8.8"]),
            ["2606:2800:220:1:248:1893:25c8:1946"])
        resolver.query.side_effect = dns.exception.UnexpectedEnd()
        self.assertEqual(resolver.nameservers, ["8.8.8.8"])
        self.assertEqual(v6wos.util.lookup.check_aaaa("example.com"), [])
        self.assertEqual(
            resolver.nameservers, v6wos.util.lookup.DEFAULT_NAMESERVERS)

    @unittest.mock.patch("dns.resolver.Resolver")
    @unittest.mock.patch("v6wos.util.lookup.check_aaaa")
    def test_check_glue(self, check_aaaa, Resolver):
        Resolver.return_value = resolver = unittest.mock.Mock()
        resolver.query.return_value = [
            unittest.mock.Mock(to_text=lambda: "a.iana-servers.net"),
            unittest.mock.Mock(to_text=lambda: "b.iana-servers.net"),
        ]
        check_aaaa.side_effect = [
            ["2001:500:8f::53"],
            ["2001:500:8d::53"],
        ]
        self.assertEqual(
            v6wos.util.lookup.check_glue("example.com", ["8.8.8.8"]),
            ["2001:500:8f::53", "2001:500:8d::53"])
        resolver.query.side_effect = dns.exception.UnexpectedEnd()
        self.assertEqual(resolver.nameservers, ["8.8.8.8"])
        self.assertEqual(v6wos.util.lookup.check_glue("example.com"), [])
        self.assertEqual(
            resolver.nameservers, v6wos.util.lookup.DEFAULT_NAMESERVERS)
