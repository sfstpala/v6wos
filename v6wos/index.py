import v6wos


class IndexHandler(v6wos.RequestHandler):

    def get(self):
        self.render("index.html")
