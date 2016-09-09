import sys
import os
import time
import glob
import pkg_resources
import v6wos.tests.integration


def main(args):
    config = args[0]
    server = v6wos.tests.integration.Server(config)
    server.start()
    filenames = glob.glob(os.path.join(pkg_resources.resource_filename(
        "v6wos", "tests"), "integration", "**", "*.md"), recursive=True)
    try:
        server.wait()
        failed = 0
        for filename in filenames:
            result = v6wos.tests.integration.testfile(filename, server)
            failed = failed or result.failed
    finally:
        time.sleep(0.1)
        server.terminate()
    return 1 if failed else 0


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: {} <config>".format(
            "bin/python -m v6wos.tests.integration"), file=sys.stderr)
        sys.exit(2)
    sys.exit(main(sys.argv[1:]))
