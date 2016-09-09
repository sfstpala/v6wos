import v6wos.tests


class IndexHandlerTest(v6wos.tests.TestCase):

    def test_get(self):
        res = self.fetch("/")
        self.assertEqual(res.code, 200)
