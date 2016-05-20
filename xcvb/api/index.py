import xcvb
import xcvb.api


class IndexHandler(xcvb.api.RequestHandler):

    def get(self):
        self.write({
            "service": xcvb.__name__,
            "version": xcvb.__version__,
        })
