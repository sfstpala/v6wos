import xcvb.api


class ErrorHandler(xcvb.api.ErrorHandler):

    def initialize(self):
        super().initialize(404)
