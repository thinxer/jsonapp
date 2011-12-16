import sys
if sys.version_info.major == 3:
    from urllib.request import Request, urlopen
else:
    from urllib2 import Request, urlopen
import json

__all__ = ['Remote']

class Remote(object):
    def __init__(self, endpoint, basename=''):
        self.__url = endpoint
        self.__methods = []
        self.__basename = basename

    def __getattr__(self, name):
        if name in ['trait_names', '_getAttributeNames']:
            return None
        if self.__basename and name:
            newname = self.__basename + '.' + name
        else:
            newname = self.__basename or name
        r = Remote(self.__url, newname)
        r.__methods = [m[len(name)+1:] for m in self.__methods if m.startswith(name + '.')]
        return r

    def __getitem__(self, name):
        return getattr(self, name)

    @property
    def __methods__(self):
        if not self.__methods:
            self.__methods = self['rpc.listMethods']()
        return self.__methods

    @property
    def __dict__(self):
        return {method: getattr(self, method) for method in self.__methods__}

    def __call__(self, *params):
        content = json.dumps({
            'method': self.__basename,
            'params': params
            }).encode('utf8')
        req = Request(self.__url, content)
        resp = urlopen(req)
        response = json.loads(resp.read().decode('utf8'))
        if 'error' in response:
            raise Exception(response['error'])
        else:
            return response['result']

    def __repr__(self):
        return '<jsonapp.Remote: \'%s\' @ %s>' % (self.__basename, self.__url)

if __name__ == '__main__':
    r = Remote("http://localhost:8080/api")
    #r.hello("JsonApp")
