import unittest.mock
import xcvb.tests
import xcvb.util


class UtilTest(xcvb.tests.TestCase):

    @unittest.mock.patch("uuid.uuid4")
    def test_random_id(self, uuid4):
        uuid4.return_value.bytes = b"\x00" * 16
        self.assertEqual(xcvb.util.random_id(), "0" * 26)

    @unittest.mock.patch("subprocess.getstatusoutput")
    def test_get_git_revision(self, getstatusoutput):
        getstatusoutput.return_value = 0, "ffffff"
        self.assertEqual(xcvb.util.get_git_revision(), "ffffff")
        getstatusoutput.return_value = 1, "error!"
        self.assertEqual(xcvb.util.get_git_revision(), "ffffff")
        xcvb.util.get_git_revision.cache_clear()
        self.assertEqual(xcvb.util.get_git_revision(), None)
