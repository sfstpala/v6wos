'''
Usage:
    xcvb [--config=<config>] [--debug]
    xcvb (--help | --version)

Options:
    --config=<config>  configuration file (*.yaml)
    --debug            enable debugging

'''

import sys
import logging
import docopt
import tornado.log
import xcvb


class LogFormatter(tornado.log.LogFormatter):

    fmt = "[%(levelname)1.1s %(process)d %(asctime)s] %(message)s"
    datefmt = "%Y-%m-%d %H:%M:%S%z"

    def __init__(self, name):
        super().__init__(
            color=False, colors={}, fmt=self.fmt, datefmt=self.datefmt)


def configure_logging(debug=False, stdout=None, stderr=None):
    log_level = "DEBUG" if debug else "INFO"
    tornado.log.enable_pretty_logging(options=type("options", (), {
        "logging": log_level,
        "log_file_prefix": None,
        "log_to_stderr": False})())
    for logger in (tornado.log.app_log, tornado.log.gen_log):
        channel = logging.StreamHandler(stream=(stderr or sys.stderr))
        channel.setFormatter(LogFormatter(logger.name))
        logger.handlers = [channel]
    channel = logging.StreamHandler(stream=(stdout or sys.stdout))
    channel.setFormatter(LogFormatter(tornado.log.access_log.name))
    tornado.log.access_log.handlers = [channel]


def main(args=None):
    try:
        args = args if args is not None else sys.argv[1:]
        args = docopt.docopt(__doc__, argv=args, version=xcvb.__version__)
    except docopt.DocoptExit as e:
        print(str(e), file=sys.stderr)
        return 2
    configure_logging(args["--debug"])
    try:
        application = xcvb.Application(
            config=args["--config"], debug=args["--debug"])
    except RuntimeError as e:
        tornado.log.app_log.error("Fatal: " + str(e))
        return 1
    try:
        xcvb.HTTPServer(application).run()
    except KeyboardInterrupt:
        return 1


if __name__ == "__main__":
    sys.exit(main())
