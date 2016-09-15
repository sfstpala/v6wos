import tornado.gen
import v6wos.api
import v6wos.model.hosts


class HostsHandler(v6wos.api.RequestHandler):

    def prepare(self):
        self.model = v6wos.model.hosts.Hosts(self.application)

    @tornado.gen.coroutine
    def get(self, name=None):
        if name is not None and name in self.model.all_hosts:
            return self.write((yield self.model.put(name)))
        if name is not None:
            raise tornado.web.HTTPError(404)
        self.write({
            "hosts": (yield self.model.get()),
        })
