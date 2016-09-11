import pkg_resources
import v6wos.api
import v6wos.util.lookup


class HostsHandler(v6wos.api.RequestHandler):

    def get(self):
        with open(pkg_resources.resource_filename(
                "v6wos", "resources/top100.txt")) as f:
            hosts = [i.strip() for i in f.readlines() if i.strip()]
            self.write({
                "hosts": hosts,
            })


class HostsDetailHandler(v6wos.api.RequestHandler):

    def get(self, host):
        self.write({
            "host": host,
            "aaaa": v6wos.util.lookup.check_aaaa(host),
        })
