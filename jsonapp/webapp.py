from router import Router
from jsonapp import JsonApplication
from staticapp import StaticFileApplication, StaticContentApplication
from redirector import Redirector

import os.path

__all__ = ["DefaultWebApplication"]

class DefaultWebApplication(Router):
    def __init__(self):
        self.staticapp = StaticFileApplication(".")
        self.jsonapp = JsonApplication()

        Router.__init__(self)
        self.route("/static/.*", self.staticapp)
        with open(os.path.join(os.path.dirname(__file__), "./client.js")) as f:
            clientjs = f.read()
        self.route("/_client.js", StaticContentApplication(clientjs))
        self.route("/api", self.jsonapp)
        self.route("/", Redirector("/static/index.html", self))
