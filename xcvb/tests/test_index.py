import xcvb.tests


class IndexHandlerTest(xcvb.tests.TestCase):

    def test_get(self):
        res = self.fetch("/")
        self.assertEqual(res.code, 200)
