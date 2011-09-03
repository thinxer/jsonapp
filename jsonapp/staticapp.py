import os
import mimetypes

__all__ = ["StaticFileApplication", "StaticContentApplication"]

class StaticFileApplication(object):
    def __init__(self, path):
        self.path = path

    def __call__(self, env, start_response):
        path = env['PATH_INFO'][1:]
        #TODO check path, potential security problem
        filepath = os.path.join(self.path, path)
        if os.path.exists(filepath):
            content_type, encoding = mimetypes.guess_type(filepath)
            headers = []
            if content_type: headers.append( ('Content-Type', content_type) )
            if encoding: headers.append( ('Content-Encoding', encoding) )
            start_response('200 OK', headers)
            with open(filepath, 'rb') as f:
                yield f.read()
        else:
            start_response('404 Not Found', [])
            yield ''

class StaticContentApplication(object):
    def __init__(self, content, content_type = None):
        self.content = content
        self.headers = []
        if content_type:
            self.headers.append( ('Content-Type', content_type) )

    def __call__(self, env, start_response):
        start_response('200 OK', self.headers)
        return self.content
