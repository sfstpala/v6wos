import xcvb
import xcvb.tests.api


class IndexHandlerTest(xcvb.tests.api.TestCase):

    def test_get(self):
        res = self.fetch("/api")
        self.assertEqual(res.code, 200)
        self.assertEqual(res.json, {
            "service": xcvb.__name__,
            "version": xcvb.__version__,
        })
