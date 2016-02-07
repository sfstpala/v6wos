import c24.tests


class ErrorHandlerTest(c24.tests.TestCase):

    def test_get(self):
        res = self.fetch("/404")
        self.assertEqual(res.code, 404)
