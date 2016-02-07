import c24


class IndexHandler(c24.RequestHandler):

    def get(self):
        self.render("index.html")
