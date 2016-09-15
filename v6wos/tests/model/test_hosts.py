import unittest.mock
import tornado.testing
import v6wos.tests
import v6wos.model.hosts


class HostsTest(v6wos.tests.TestCase):

    @unittest.mock.patch("couch.AsyncCouch.view")
    @unittest.mock.patch("v6wos.model.hosts.Hosts.put")
    @unittest.mock.patch("v6wos.model.hosts.Hosts.delete")
    @tornado.testing.gen_test
    def test_get(self, delete, put, view):
        delete.return_value = v6wos.tests.future()
        put.return_value = v6wos.tests.future({
            "aaaa": [
                "2a03:2880:1020:3f83:face:b00c::25de",
            ],
            "name": "facebook.com",
        })
        view.return_value = v6wos.tests.future({
            "rows": [
                {
                    "value": {
                        "host": {
                            "aaaa": [],
                            "name": "example.invalid",
                        },
                        "type": "host",
                    },
                },
                {
                    "value": {
                        "host": {
                            "aaaa": [
                                "2a00:1450:4001:817::200e",
                            ],
                            "name": "google.com",
                        },
                        "type": "host",
                    },
                },
            ],
        })
        model = v6wos.model.hosts.Hosts(self.application)
        model.all_hosts = ["google.com", "facebook.com"]
        res = yield model.get()
        self.assertEqual(res, [
            {
                "aaaa": [
                    "2a00:1450:4001:817::200e",
                ],
                "name": "google.com",
            },
            {
                "aaaa": [
                    "2a03:2880:1020:3f83:face:b00c::25de",
                ],
                "name": "facebook.com",
            },
        ])

    @unittest.mock.patch("couch.AsyncCouch.view")
    @unittest.mock.patch("couch.AsyncCouch.save_doc")
    @unittest.mock.patch("v6wos.util.lookup.check_aaaa")
    @tornado.testing.gen_test
    def test_put(self, check_aaaa, save_doc, view):
        check_aaaa.return_value = [
            "2a00:1450:4001:817::200e",
        ]
        save_doc.return_value = v6wos.tests.future()
        view.return_value = v6wos.tests.future({
            "rows": [
                {
                    "value": {
                        "_id": "100",
                        "_rev": "100-1",
                        "host": {
                            "aaaa": [],
                            "name": "google.com",
                        },
                        "type": "host",
                    },
                },
            ],
        })
        model = v6wos.model.hosts.Hosts(self.application)
        res = yield model.put("google.com")
        self.assertEqual(res, {
            "aaaa": [
                "2a00:1450:4001:817::200e",
            ],
            "name": "google.com",
        })
        save_doc.assert_called_once_with({
            "_id": "100",
            "_rev": "100-1",
            "host": {
                "aaaa": [
                    "2a00:1450:4001:817::200e",
                ],
                "name": "google.com",
            },
            "type": "host",
        })

    @unittest.mock.patch("couch.AsyncCouch.view")
    @unittest.mock.patch("couch.AsyncCouch.delete_docs")
    @tornado.testing.gen_test
    def test_delete(self, delete_docs, view):
        delete_docs.return_value = v6wos.tests.future()
        view.return_value = v6wos.tests.future({
            "rows": [
                {
                    "value": {
                        "_id": "200",
                        "_rev": "200-1",
                        "host": {
                            "aaaa": [],
                            "name": "example.invalid",
                        },
                        "type": "host",
                    },
                },
            ],
        })
        model = v6wos.model.hosts.Hosts(self.application)
        yield model.delete("example.invalid")
        delete_docs.assert_called_once_with([{
            "_id": "200",
            "_rev": "200-1",
            "host": {
                "aaaa": [],
                "name": "example.invalid",
            },
            "type": "host",
        }])
