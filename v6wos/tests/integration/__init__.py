import doctest
import json
import functools
import operator
import time
import multiprocessing
import requests
import v6wos

from v6wos.__main__ import main


OPTIONFLAGS = [
    doctest.ELLIPSIS,
    doctest.REPORT_NDIFF,
    doctest.IGNORE_EXCEPTION_DETAIL,
    doctest.NORMALIZE_WHITESPACE,
]


class Server(multiprocessing.Process):

    def __init__(self, config):
        self.config = config
        self.port = v6wos.Application(
            config=self.config).config["bind"]["port"]
        self.host = "localhost:{}".format(self.port)
        super().__init__()

    def run(self):
        main(["--config", self.config])

    def wait(self):
        exception = None
        for i in range(50):
            try:
                requests.get("http://{}/".format(self.host))
            except Exception as e:
                time.sleep(0.1)
                exception = e
            else:
                exception = None
                break
        if exception is not None:
            raise exception


def dump(obj):
    print(json.dumps(obj, indent=4, sort_keys=True))


def testfile(filename, server):
    result = doctest.testfile(
        filename,
        module_relative=False,
        optionflags=functools.reduce(operator.or_, OPTIONFLAGS, 0),
        extraglobs={
            "port": server.port,
            "host": server.host,
            "config": server.config,
            "requests": requests,
            "dump": dump,
            "request": lambda method, path, **kw: requests.request(
                method, "http://{}{}".format(server.host, path), **kw),
            "get": lambda path, **kw: requests.get(
                "http://{}{}".format(server.host, path), **kw),
            "head": lambda path, **kw: requests.head(
                "http://{}{}".format(server.host, path), **kw),
            "put": lambda path, **kw: requests.put(
                "http://{}{}".format(server.host, path), **kw),
            "post": lambda path, **kw: requests.post(
                "http://{}{}".format(server.host, path), **kw),
            "delete": lambda path, **kw: requests.delete(
                "http://{}{}".format(server.host, path), **kw),
            "patch": lambda path, **kw: requests.patch(
                "http://{}{}".format(server.host, path), **kw),
            "options": lambda path, **kw: requests.options(
                "http://{}{}".format(server.host, path), **kw),
        })
    return result
