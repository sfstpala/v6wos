import tornado.gen
import v6wos


class IndexHandler(v6wos.RequestHandler):

    @tornado.gen.coroutine
    def get(self):
        res = yield self.fetch("/api/hosts")
        if res.code != 200:
            raise tornado.web.HTTPError(503)
        self.render("index.html", hosts=res.json["hosts"])
