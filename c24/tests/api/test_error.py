import c24.tests.api


class ErrorHandlerTest(c24.tests.api.TestCase):

    def test_get(self):
        res = self.fetch("/api/404")
        self.assertEqual(res.code, 404)
        self.assertEqual(res.json, {
            "status": 404,
            "reason": "not found",
        })
