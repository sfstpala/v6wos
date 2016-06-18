import unittest
import unittest.mock
import sys
import io
import copy
import os.path
import logging
import pkg_resources
import tornado.log
import xcvb.tests
import xcvb
import xcvb.tests
import xcvb.__main__


class EntryPointTest(xcvb.tests.TestCase):

    dist = pkg_resources.get_distribution(__package__.split(".")[0])
    main = staticmethod(dist.load_entry_point("console_scripts", "xcvb"))

    @unittest.mock.patch("xcvb.HTTPServer.run")
    @unittest.mock.patch("xcvb.Application.load_config")
    @unittest.mock.patch("xcvb.__main__.configure_logging")
    @unittest.mock.patch("tornado.ioloop.IOLoop.current")
    def test_main(self, current, configure_logging, load_config, run):
        load_config.return_value = copy.deepcopy(self.config)
        load_config.return_value["security"]["cookie-secret"] = "insecure"
        load_config.return_value["database"]["postgres"] = "sqlite:///:memory:"
        run.side_effect = KeyboardInterrupt()
        self.assertEqual(self.main([]), 1)
        run.assert_called_once_with()
        configure_logging.assert_called_once_with(False)

    @unittest.mock.patch("builtins.print")
    def test_invalid_argument(self, print):
        self.assertEqual(self.main(["--invalid-argument"]), 2)
        print.assert_called_once_with(
            xcvb.__main__.__doc__.split(
                "\n\n")[0].strip(), file=sys.stderr)


class LogTest(xcvb.tests.TestCase):

    def test_configure_logging(self):
        stdout = io.StringIO()
        stderr = io.StringIO()
        xcvb.__main__.configure_logging(
            debug=True, stdout=stdout, stderr=stderr)
        self.assertEqual(
            tornado.log.gen_log.getEffectiveLevel(),
            logging.DEBUG)
        self.assertEqual(
            tornado.log.app_log.getEffectiveLevel(),
            logging.DEBUG)
        self.assertEqual(
            tornado.log.access_log.getEffectiveLevel(),
            logging.DEBUG)
        tornado.log.app_log.info("log message")
        self.assertRegex(
            stderr.getvalue(), r"\[I \d+ .+\] log message$")
        tornado.log.access_log.info("log message")
        self.assertRegex(
            stdout.getvalue(), r"\[I \d+ .+\] log message$")


if __name__ == "__main__":
    os.chdir(os.path.split(os.path.split(xcvb.__file__)[0])[0])
    sys.exit(os.system(sys.executable + " setup.py test"))
