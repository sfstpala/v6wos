import c24.tests


class IndexHandlerTest(c24.tests.TestCase):

    def test_get(self):
        res = self.fetch("/")
        self.assertEqual(res.code, 200)
