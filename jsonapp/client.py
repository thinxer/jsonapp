import urllib2
import json
import hashlib

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
            self._methods = map(str, self._request('rpc.listMethods'))
        return self._methods

    def _request(self, name, params = []):
        req = urllib2.Request(self._url, json.dumps({
            'method': name,
            'params': params
            }))
        resp = urllib2.urlopen(req)
        response = json.load(resp)
        if 'error' in response:
            raise Exception(response['error'])
        else:
            return response['result']

    def _generalmethod(self, name):
        def generalmethod(*args):
            return self._request(name, args)
        generalmethod.func_name = name
        return generalmethod

#r = Remote("http://localhost:8080/api")
#r.hello("JsonApp")
