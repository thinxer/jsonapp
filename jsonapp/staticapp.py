import os

__all__ = ["StaticFileApplication", "StaticContentApplication"]

class StaticFileApplication(object):
    def __init__(self, path):
        self.path = path

    def __call__(self, env, start_response):
        path = env['PATH_INFO'][1:]
        #TODO check path, potential security problem
        filepath = os.path.join(self.path, path)
        if os.path.exists(filepath):
            start_response('200 OK', [])
            with open(filepath, 'rb') as f:
                return [f.read()]
        else:
            start_response('404 Not Found', [])
            return ['']

class StaticContentApplication(object):
    def __init__(self, content):
        self.content = content

    def __call__(self, env, start_response):
        start_response('200 OK', [])
        return self.content
