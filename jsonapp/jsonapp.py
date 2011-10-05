import json
import traceback

__all__ = ['JsonApplication']

class JsonApplication(object):

    def __init__(self, jsonencoder = None, jsondecoder = None):
        self.handlers = {}
        self.register(self.list_methods, 'rpc.listMethods')
        if jsonencoder:
            self.dumps = jsonencoder
        else:
            self.dumps = json.dumps
        if jsondecoder:
            self.loads = jsondecoder
        else:
            self.loads = json.loads

    def list_methods(self):
        return list(self.handlers.keys())

    def register(self, func, path = None):
        if not path:
            path = func.__name__
        self.handlers[path] = func
        return func

    def decorator(self, func = None):
        if isinstance(func, str):
            path = func
            return lambda func: self.register(func, path)
        else:
            return self.register(func)

    def __call__(self, env, start_response):
        method = env.get('REQUEST_METHOD', 'GET')
        if method != 'POST':
            start_response('400 Bad Request', [])
            return []
        cookie = env.get('HTTP_COOKIE')
        length = int(env.get('CONTENT_LENGTH', -1))
        raw_data = env['wsgi.input'].read(length)
        try:
            request = self.loads(raw_data.decode('utf8'))
        except:
            traceback.print_exc()
            start_response('400 Bad Request', [])
            return []

        start_response('200 OK', [('Content-Type', 'application/json')])
        rid = request.get('id')
        ret = {}
        if rid: ret['id'] = rid
        try:
            method = request['method']
            params = request['params']
            ret['result'] = self.handlers[method](*params)
        except Exception as e:
            traceback.print_exc()
            ret['error'] = str(e)
        return [self.dumps(ret).encode('utf8')]

def test():
    application = JsonApplication()
    api = application.decorator

    @api
    def add(x, y):
        return x + y

    @api("m")
    def mul(x, y):
        return x * y

    from server import serve
    serve(application)

if __name__ == '__main__':
    test()
