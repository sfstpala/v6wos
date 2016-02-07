import c24.api


class IndexHandler(c24.api.RequestHandler):

    def get(self):
        self.write({})
