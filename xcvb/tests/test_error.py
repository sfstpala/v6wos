import xcvb.tests


class ErrorHandlerTest(xcvb.tests.TestCase):

    def test_get(self):
        res = self.fetch("/404")
        self.assertEqual(res.code, 404)
