import re

__all__ = ['Router']

class Router(object):
    def __init__(self):
        self.handlers = []

    def __call__(self, env, start_response):
        path = env['PATH_INFO']
        for pattern, app in self.handlers:
            if pattern.match(path):
                return app(env, start_response)

        start_response('404 Not Found', [])
        return ['']

    def route(self, path, app):
        self.handlers.append( (re.compile('^' + path + '$'), app) )
