try:
    import json
except:
    from django.utils import simplejson as json

__all__ = ['JsonApplication']

class JsonApplication(object):

    def __init__(self):
        self.handlers = {}

    def register(self, func, path = None):
        if not path:
            path = func.func_name
        self.handlers[path] = func

    def decorator(self, func = None):
        if isinstance(func, str):
            path = func
            return lambda func: self.register(func, path)
        else:
            self.register(func)

    def __call__(self, env, start_response):
        method = env.get('REQUEST_METHOD', 'GET')
        if method != 'POST':
            start_response('400 Bad Request', [])
            return []
        cookie = env.get('HTTP_COOKIE')
        raw_data = env['wsgi.input'].read()
        start_response('200 OK', []);
        try:
            request = json.loads(raw_data)
        except:
            start_response('400 Bad Request', [])
            return []

        rid = request.get('id')
        ret = {}
        if rid: ret['id'] = rid
        try:
            method = request['method']
            params = request['params']
            ret['result'] = self.handlers[method](*params)
        except Exception, e:
            ret['error'] = str(e)
        return [json.dumps(ret)]

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
