import pkg_resources
import tornado.gen
import v6wos.model
import v6wos.util.lookup


class Hosts(v6wos.model.Base):

    with open(pkg_resources.resource_filename(
            "v6wos", "resources/hosts.txt")) as f:
        all_hosts = [i.strip() for i in f.readlines() if i.strip()]

    @tornado.gen.coroutine
    def get(self):
        res = yield self.couch.view("hosts", "by_name")
        res = [i["value"]["host"] for i in res["rows"]]
        for i in self.all_hosts:
            if i not in [doc["name"] for doc in res]:
                res.append((yield self.put(i)))
        for i in [doc["name"] for doc in res]:
            if i not in self.all_hosts:
                yield self.delete(i)
        dup = set()
        res = [i for i in res
               if i["name"] in self.all_hosts
               and i["name"] not in dup
               and not dup.add(i["name"])]
        res = list(sorted(res, key=lambda i: self.all_hosts.index(i["name"])))
        return res

    @tornado.gen.coroutine
    def put(self, name):
        res = yield self.couch.view("hosts", "by_name", key=str(name))
        doc = res["rows"][0]["value"] if res["rows"] else {}
        nameservers = self.application.config["dns"]["nameservers"]
        doc.update({
            "host": {
                "name": name,
                "aaaa": v6wos.util.lookup.check_aaaa(
                    name, nameservers=nameservers),
                "glue": v6wos.util.lookup.check_glue(
                    name, nameservers=nameservers),
            },
            "type": "host",
        })
        yield self.couch.save_doc(doc)
        return doc["host"]

    @tornado.gen.coroutine
    def delete(self, name):
        res = yield self.couch.view("hosts", "by_name", key=str(name))
        yield self.couch.delete_docs([i["value"] for i in res["rows"]])
