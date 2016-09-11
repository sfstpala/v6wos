import tornado.gen
import v6wos


class IndexHandler(v6wos.RequestHandler):

    @tornado.gen.coroutine
    def get_hosts(self):
        res = yield self.fetch("/api/hosts")
        if res.code != 200:
            raise tornado.web.HTTPError(503)
        return res.json

    @tornado.gen.coroutine
    def get_host(self, host):
        res = yield self.fetch("/api/hosts/" + host)
        if res.code != 200:
            raise tornado.web.HTTPError(503)
        return res.json

    @tornado.gen.coroutine
    def get(self):
        hosts = []
        for i in (yield self.get_hosts())["hosts"]:
            if i not in self.application.hosts_cache:
                host = yield self.get_host(i)
                self.application.hosts_cache[i] = host
            hosts.append(self.application.hosts_cache[i])
        self.render("index.html", hosts=hosts)
