import pkg_resources
import tornado.web
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
        nameservers = self.application.config["dns"]["nameservers"]
        with open(pkg_resources.resource_filename(
                "v6wos", "resources/top100.txt")) as f:
            hosts = [i.strip() for i in f.readlines() if i.strip()]
        if host not in hosts:
            raise tornado.web.HTTPError(404)
        self.application.hosts_cache[host] = {
            "host": host,
            "aaaa": v6wos.util.lookup.check_aaaa(
                host, nameservers=nameservers),
        }
        self.write(self.application.hosts_cache[host])