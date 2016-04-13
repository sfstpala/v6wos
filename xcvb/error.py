import xcvb


class ErrorHandler(xcvb.ErrorHandler):

    def initialize(self):
        super().initialize(404)
