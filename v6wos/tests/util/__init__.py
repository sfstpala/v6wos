import unittest.mock
import v6wos.tests
import v6wos.util


class UtilTest(v6wos.tests.TestCase):

    def test_b32encode(self):
        self.assertEqual(v6wos.util.b32encode(0), "0")
        self.assertEqual(v6wos.util.b32encode(1), "1")
        self.assertEqual(v6wos.util.b32encode(32), "10")
        self.assertEqual(v6wos.util.b32encode(64), "20")
        self.assertEqual(v6wos.util.b32encode(127), "3z")

    @unittest.mock.patch("uuid.uuid4")
    def test_random_id(self, uuid4):
        uuid4.return_value.bytes = b"\x00" * 16
        self.assertEqual(v6wos.util.random_id(), "00000000000000000000000000")
        uuid4.return_value.bytes = b"\xFF" * 16
        self.assertEqual(v6wos.util.random_id(), "7zzzzzzzzzzzzzzzzzzzzzzzzz")

    @unittest.mock.patch("subprocess.getstatusoutput")
    def test_get_git_revision(self, getstatusoutput):
        getstatusoutput.return_value = 0, "ffffff"
        self.assertEqual(v6wos.util.get_git_revision(), "ffffff")
        getstatusoutput.return_value = 1, "error!"
        self.assertEqual(v6wos.util.get_git_revision(), "ffffff")
        v6wos.util.get_git_revision.cache_clear()
        self.assertEqual(v6wos.util.get_git_revision(), None)
