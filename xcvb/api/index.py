import xcvb
import xcvb.util
import xcvb.api


class IndexHandler(xcvb.api.RequestHandler):

    def get(self):
        service = xcvb.__name__
        version = "{} ({})".format(
            xcvb.__version__, xcvb.util.get_git_revision()
        ) if xcvb.util.get_git_revision() else xcvb.__version__
        self.write({
            "service": service,
            "version": version,
        })
