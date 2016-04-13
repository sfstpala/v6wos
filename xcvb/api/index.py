import xcvb.api


class IndexHandler(xcvb.api.RequestHandler):

    def get(self):
        self.write({})
