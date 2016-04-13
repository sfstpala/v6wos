import xcvb


class IndexHandler(xcvb.RequestHandler):

    def get(self):
        self.render("index.html")
