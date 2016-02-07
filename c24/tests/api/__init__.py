import unittest.mock
import json
import c24.tests
import c24.api


class TestCase(c24.tests.TestCase):

    def fetch(self, *args, **kwargs):
        response = super().fetch(*args, **kwargs)
        try:
            response.json = json.loads((response.body or b"").decode())
        except ValueError:
            pass
        return response


class TestHandler(c24.api.RequestHandler):

    @c24.api.schema({
        "type": "object",
        "properties": {
            "test": {
                "type": "number",
            },
        },
    })
    def post(self):
        self.write(self.body)

    def options(self):
        self.write(b"")


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

    def test_schema(self):
        res = self.fetch("/test", body={"test": 1}, method="POST")
        self.assertEqual(res.code, 200)
        self.assertEqual(res.json, {"test": 1})
        res = self.fetch("/test", body=b'', method="POST")
        self.assertEqual(res.code, 422)
        res = self.fetch("/test", body=b'{"test": ', method="POST")
        self.assertEqual(res.code, 400)
        res = self.fetch("/test", body=b'[]', method="POST")
        self.assertEqual(res.code, 400)

    def test_body(self):
        res = self.fetch("/test", method="OPTIONS")
        self.assertEqual(res.code, 200)
        self.assertEqual(res.body, b"")
