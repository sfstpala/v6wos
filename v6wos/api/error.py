import v6wos.api


class ErrorHandler(v6wos.api.ErrorHandler):

    def initialize(self):
        super().initialize(404)
