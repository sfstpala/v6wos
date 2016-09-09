import v6wos


class ErrorHandler(v6wos.ErrorHandler):

    def initialize(self):
        super().initialize(404)
