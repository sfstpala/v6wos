import v6wos.tests


class ErrorHandlerTest(v6wos.tests.TestCase):

    def test_get(self):
        res = self.fetch("/404")
        self.assertEqual(res.code, 404)
