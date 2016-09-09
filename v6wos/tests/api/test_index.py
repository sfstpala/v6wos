import unittest.mock
import v6wos
import v6wos.tests.api


class IndexHandlerTest(v6wos.tests.api.TestCase):

    @unittest.mock.patch("v6wos.util.get_git_revision")
    def test_get(self, get_git_revision):
        get_git_revision.return_value = "ffffff"
        res = self.fetch("/api")
        self.assertEqual(res.code, 200)
        self.assertEqual(res.json, {
            "service": v6wos.__name__,
            "version": v6wos.__version__ + " (ffffff)",
        })
