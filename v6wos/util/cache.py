import time
import concurrent.futures
import pkg_resources
import tornado.log


class HostsCache(dict):

    log = tornado.log.app_log
    max_workers = 80

    def get_hosts(self):
        with open(pkg_resources.resource_filename(
                "v6wos", "resources/top100.txt")) as f:
            return [i.strip() for i in f.readlines() if i.strip()]

    def warmup(self, nameservers):
        self.log.info("Warming up caches...")
        t = time.time()
        with concurrent.futures.ThreadPoolExecutor(
                max_workers=self.max_workers) as e:
            for i in e.map(lambda host: self.__setitem__(host, {
                "host": host,
                "aaaa": tornado.util.import_object(
                    "v6wos.util.lookup.check_aaaa")(
                        host, nameservers=nameservers),
            }), self.get_hosts()):
                pass
        self.log.info("Warming up caches finished ({:.1f} seconds)".format(
            time.time() - t))
