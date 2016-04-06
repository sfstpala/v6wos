import os
import copy
import uuid
import functools
import base64
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


def random_id(seed=None):
    seed = seed or uuid.uuid4().bytes
    return base64.urlsafe_b64encode(seed).decode().rstrip("=")


class RequestHandler(tornado.web.RequestHandler):

    def set_default_headers(self):
        self.set_header("Server", "C24/" + __version__)

    def write_error(self, status, reason=None, detail=None, **kwargs):
        reason = reason or http.client.responses.get(status)
        self.render("error.html", status=status, reason=reason)

    def prepare(self):
        super().prepare()
        self.request.session_id = self.get_session_id()
        self.request.dnt = self.request.headers.get("DNT", "0") == "1"
        path, query = (self.request.path or "/")[1:], self.request.query
        if path.endswith("/"):
            if self.request.method in ("GET", "HEAD", "OPTIONS"):
                path = "/" + path[:-1] + (("?" + query) if query else "")
                return self.redirect(path, permanent=True)

    @functools.lru_cache()
    def get_session_id(self):
        cookie = self.get_secure_cookie("session-id") or None
        cookie = (cookie or b"").decode("ascii", errors="replace") or None
        cookie = (cookie or random_id())
        self.set_secure_cookie("session-id", cookie)
        return cookie

    def set_secure_cookie(self, name, value):
        expires_days = (
            self.application.config["security"]["cookie-expiry"])
        super().set_secure_cookie(name, value, expires_days=expires_days)

    def get_secure_cookie(self, name, value=None):
        max_age_days = (
            self.application.config["security"]["cookie-expiry"]) + 1
        return super().get_secure_cookie(
            name, value, max_age_days=max_age_days)

    def get_template_namespace(self):
        self.ui = self.ui or {}
        namespace = super().get_template_namespace() or {}
        namespace.update({
            "debug": self.application.settings["debug"],
            "service": __name__,
            "version": __version__,
        })
        return namespace


class ErrorHandler(RequestHandler, tornado.web.ErrorHandler):

    pass


class Application(tornado.web.Application):

    handlers = [
        (r"/?", tornado.util.import_object(
            "c24.index.IndexHandler")),
        (r"/api/?", tornado.util.import_object(
            "c24.api.index.IndexHandler")),
        (r"/api/.*?", tornado.util.import_object(
            "c24.api.error.ErrorHandler")),
        (r".*", tornado.util.import_object(
            "c24.error.ErrorHandler")),
    ]

    log = tornado.log.app_log

    settings = {
        "template_path": pkg_resources.resource_filename(
            "c24", "templates"),
        "static_path": pkg_resources.resource_filename(
            "c24", "static"),
        "xsrf_cookies": True,
    }

    with open(pkg_resources.resource_filename(
            "c24", "config/local.yaml")) as f:
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
        self.log.info("Loading " + (filename or "default configuration"))
        config = copy.deepcopy(self.default_config)
        if os.path.exists(filename):
            with open(filename) as f:
                update_recursive(config, yaml.load(f))
        else:
            with open(filename, "w") as f:
                f.write(yaml.dump(
                    self.default_config, default_flow_style=False))
        tornado.autoreload.watch(filename)
        return {k: v for k, v in config.items()
                if k in dict(self.default_config)}

    def update_settings(self, config):
        cookie_uuid = config["security"]["cookie-secret"]
        if cookie_uuid is None and not self.settings["debug"]:
            raise RuntimeError("cookie-secret must be set in production mode")
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
