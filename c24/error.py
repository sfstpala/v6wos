import c24


class ErrorHandler(c24.ErrorHandler):

    def initialize(self):
        super().initialize(404)
