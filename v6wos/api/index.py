import v6wos
import v6wos.util
import v6wos.api


class IndexHandler(v6wos.api.RequestHandler):

    def get(self):
        service = v6wos.__name__
        version = "{} ({})".format(
            v6wos.__version__, v6wos.util.get_git_revision()
        ) if v6wos.util.get_git_revision() else v6wos.__version__
        self.write({
            "service": service,
            "version": version,
        })
