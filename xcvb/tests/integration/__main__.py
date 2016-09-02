import sys
import os
import time
import glob
import pkg_resources
import xcvb.tests.integration


def main(args):
    config = args[0]
    server = xcvb.tests.integration.Server(config)
    server.start()
    filenames = glob.glob(os.path.join(pkg_resources.resource_filename(
        "xcvb", "tests"), "integration", "**", "*.md"), recursive=True)
    try:
        server.wait()
        failed = 0
        for filename in filenames:
            result = xcvb.tests.integration.testfile(filename, server)
            failed = failed or result.failed
    finally:
        time.sleep(0.1)
        server.terminate()
    return 1 if failed else 0


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: {} <config>".format(
            "bin/python -m xcvb.tests.integration"), file=sys.stderr)
        sys.exit(2)
    sys.exit(main(sys.argv[1:]))
