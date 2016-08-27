import http.client
import json
import functools
import tornado.web
import jsonschema
import xcvb


def schema(input_schema):
    def decorator(fn):
        @functools.wraps(fn)
        def wrapped(self, *a, **kw):
            try:
                jsonschema.validate(self.body, input_schema)
            except jsonschema.ValidationError as e:
                self.set_status(422)
                self.write_error(
                    422, reason="validation failed", detail=e.message)
                return
            return fn(self, *a, **kw)
        return wrapped
    return decorator


class RequestHandler(xcvb.RequestHandler):

    def write(self, obj):
        if isinstance(obj, dict):
            self.set_header("Content-Type", "application/json; charset=UTF-8")
            obj = json.dumps(obj, indent=4, sort_keys=True).encode() + b"\n"
        super().write(obj)

    def write_error(self, status, reason=None, detail=None, **kwargs):
        reason = reason or http.client.responses.get(status, "")
        self.write({k: v for k, v in ({
            "status": status,
            "reason": reason.lower() or None,
            "detail": detail,
        }).items() if v is not None})

    @property
    def body(self):
        try:
            body = self.request.body.decode("UTF-8")
            if not body:
                return body
            body = json.loads(body)
            if not isinstance(body, dict):
                self.set_status(400)
                self.write_error(400, reason="body should be a json object")
                raise tornado.web.Finish()
        except ValueError:
            self.set_status(400)
            self.write_error(400, reason="problems parsing json")
            raise tornado.web.Finish()
        return body

    def check_xsrf_cookie(self):
        pass


class ErrorHandler(RequestHandler, xcvb.ErrorHandler):

    pass
