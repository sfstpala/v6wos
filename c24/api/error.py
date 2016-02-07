import c24.api


class ErrorHandler(c24.api.ErrorHandler):

    def initialize(self):
        super().initialize(404)
