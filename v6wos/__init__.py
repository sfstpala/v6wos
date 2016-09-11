import os
import copy
import uuid
import json
import traceback
import collections
import http.client
import pkg_resources
import yaml
import tornado.web
import tornado.gen
import tornado.log
import tornado.util
import tornado.autoreload
import tornado.httpserver
import tornado.httpclient


__version__ = pkg_resources.get_distribution(__package__).version


class RequestHandler(tornado.web.RequestHandler):

    def set_default_headers(self):
        self.set_header("Server", "v6wos/" + __version__)

    def write_error(self, status, reason=None, exc_info=None, **kwargs):
        reason = reason or http.client.responses.get(status)
        self.render(
            "error.html", status=status, reason=reason, traceback="".join(
                traceback.format_exception(*exc_info)) if exc_info else None)

    def prepare(self):
        super().prepare()
        path, query = (self.request.path or "/")[1:], self.request.query
        if path.endswith("/"):
            if self.request.method in ("GET", "HEAD", "OPTIONS"):
                path = "/" + path[:-1] + (("?" + query) if query else "")
                return self.redirect(path, permanent=True)

    def get_template_namespace(self):
        self.ui = self.ui or {}
        namespace = super().get_template_namespace() or {}
        namespace.update({
            "debug": self.application.settings["debug"],
            "service": __name__,
            "version": __version__,
        })
        return namespace

    def get_http_client(self):
        return tornado.httpclient.AsyncHTTPClient()

    @tornado.gen.coroutine
    def fetch(self, path, **kwargs):
        hostname = self.application.config["internal"]["hostname"]
        default_headers = ["Cookie", "DNT"]
        kwargs["headers"] = kwargs.get("headers", {})
        kwargs["headers"].update(
            {k: self.request.headers.get(k) for k in default_headers})
        kwargs["raise_error"] = kwargs.get("raise_error", False)
        url = self.request.protocol + "://" + (hostname or self.request.host)
        url = url + "/" + path.lstrip("/")
        response = yield self.get_http_client().fetch(url, **kwargs)
        try:
            response.json = json.loads((response.body or b"").decode())
        except json.decoder.JSONDecodeError:
            response.json = None
        return response


class ErrorHandler(RequestHandler, tornado.web.ErrorHandler):

    pass


class Application(tornado.web.Application):

    handlers = [
        (r"/?", tornado.util.import_object(
            "v6wos.index.IndexHandler")),
        (r"/fail/?", tornado.util.import_object(
            "v6wos.index.IndexHandler")),
        (r"/api/?", tornado.util.import_object(
            "v6wos.api.index.IndexHandler")),
        (r"/api/hosts/?", tornado.util.import_object(
            "v6wos.api.hosts.HostsHandler")),
        (r"/api/hosts/([^/]+)/?", tornado.util.import_object(
            "v6wos.api.hosts.HostsDetailHandler")),
        (r"/api/.*?", tornado.util.import_object(
            "v6wos.api.error.ErrorHandler")),
        (r".*", tornado.util.import_object(
            "v6wos.error.ErrorHandler")),
    ]

    log = tornado.log.app_log

    settings = {
        "template_path": pkg_resources.resource_filename(
            "v6wos", "templates"),
        "static_path": pkg_resources.resource_filename(
            "v6wos", "static"),
        "xsrf_cookies": True,
    }

    hosts_cache = {}

    with open(pkg_resources.resource_filename(
            "v6wos", "config/local.yaml")) as f:
        default_config = yaml.load(f)

    def __init__(self, config, debug=False):
        super().__init__(self.handlers, debug=debug, **self.settings)
        self.config_path = config
        self.config = self.load_config(config)
        self.update_settings(self.config)

    def load_config(self, filename):
        def update_recursive(target, update):
            for k, v in (update or {}).items():
                if isinstance(v, collections.Mapping):
                    target[k] = update_recursive(target.get(k, {}), v)
                else:
                    target[k] = update[k]
            return target
        filename = os.path.abspath(filename) if filename is not None else None
        self.log.info("Loading " + (filename or "default configuration"))
        config = copy.deepcopy(self.default_config)
        if filename is not None and os.path.exists(filename):
            with open(filename) as f:
                update_recursive(config, yaml.load(f))
        if filename is not None and not os.path.exists(filename):
            with open(filename, "w") as f:
                f.write(yaml.dump(
                    self.default_config, default_flow_style=False))
        tornado.autoreload.watch(filename)
        return {k: v for k, v in config.items()
                if k in dict(self.default_config)}

    def update_settings(self, config):
        cookie_uuid = config["security"]["cookie-secret"]
        if cookie_uuid is None:
            cookie_uuid = uuid.uuid4().hex
            self.log.warning("Using random cookie-secret: " + cookie_uuid)
        self.settings["cookie_secret"] = cookie_uuid


class HTTPServer(tornado.httpserver.HTTPServer):

    log = tornado.log.app_log

    def __init__(self, application):
        self.application = application
        xheaders = application.config["http"]["x-forwarded"]
        timeout = self.application.config["http"]["req-timeout"]
        max_clients = self.application.config["http"]["max-clients"]
        tornado.httpclient.AsyncHTTPClient.configure(
            None, max_clients=max_clients)
        super().initialize(
            self.application, xheaders=xheaders,
            idle_connection_timeout=timeout,
            body_timeout=timeout)

    def bind(self):
        port = self.application.config["bind"]["port"]
        address = self.application.config["bind"]["addr"] or None
        backlog = self.application.config["http"]["tcp-backlog"]
        super().bind(int(port), address=address, backlog=int(backlog))
        address = "[{}]".format(address) if ":" in address else address
        self.log.info("Listening on {}:{}".format(address or "[::]", port))

    def run(self, io_loop=None):
        self.bind()
        sockets = self._pending_sockets
        self._pending_sockets = []
        self.add_sockets(sockets)
        (io_loop or tornado.ioloop.IOLoop.instance()).start()
