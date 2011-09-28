import sys
if sys.version_info.major == 3:
    from urllib.request import Request, urlopen
else:
    from urllib2 import Request, urlopen
import json

__all__ = ['Remote']

class Remote(object):
    def __init__(self, endpoint):
        self._url = endpoint
        self._methods = []

    def __getattr__(self, name):
        if name not in self.__methods__:
            return None
        return self._generalmethod(name)

    def __getitem__(self, name):
        return getattr(self, name)

    @property
    def __methods__(self):
        if not self._methods:
            self._methods = self._request('rpc.listMethods')
        return self._methods

    @property
    def __dict__(self):
        return {method: getattr(self, method) for method in self.__methods__}

    def _request(self, name, params = []):
        content = json.dumps({
            'method': name,
            'params': params
            }).encode('utf8')
        req = Request(self._url, content)
        resp = urlopen(req)
        response = json.loads(resp.read().decode('utf8'))
        if 'error' in response:
            raise Exception(response['error'])
        else:
            return response['result']

    def _generalmethod(self, name):
        def generalmethod(*args):
            return self._request(name, args)
        generalmethod.__name__ = name
        return generalmethod

if __name__ == '__main__':
    r = Remote("http://localhost:8080")
    #r.hello("JsonApp")
