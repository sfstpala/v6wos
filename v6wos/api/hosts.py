import tornado.web
import v6wos.api
import v6wos.util.lookup


class HostsHandler(v6wos.api.RequestHandler):

    def get(self):
        hosts = self.application.hosts_cache.get_hosts()
        self.write({
            "hosts": hosts,
        })


class HostsDetailHandler(v6wos.api.RequestHandler):

    def get(self, host):
        nameservers = self.application.config["dns"]["nameservers"]
        hosts = self.application.hosts_cache.get_hosts()
        if host not in hosts:
            raise tornado.web.HTTPError(404)
        self.application.hosts_cache[host] = {
            "host": host,
            "aaaa": v6wos.util.lookup.check_aaaa(
                host, nameservers=nameservers),
        }
        self.write(self.application.hosts_cache[host])
