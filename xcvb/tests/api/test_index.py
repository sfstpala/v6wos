import unittest.mock
import xcvb
import xcvb.tests.api


class IndexHandlerTest(xcvb.tests.api.TestCase):

    @unittest.mock.patch("xcvb.util.get_git_revision")
    def test_get(self, get_git_revision):
        get_git_revision.return_value = "ffffff"
        res = self.fetch("/api")
        self.assertEqual(res.code, 200)
        self.assertEqual(res.json, {
            "service": xcvb.__name__,
            "version": xcvb.__version__ + " (ffffff)",
        })
