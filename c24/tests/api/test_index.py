import c24.tests.api


class IndexHandlerTest(c24.tests.api.TestCase):

    def test_get(self):
        res = self.fetch("/api")
        self.assertEqual(res.code, 200)
        self.assertEqual(res.json, {})
