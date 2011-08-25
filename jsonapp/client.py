import urllib2
import json
import hashlib

__all__ = ['Remote']

class Remote(object):
    def __init__(self, endpoint):
        self._url = endpoint

    def __getattr__(self, name):
        return self._dumbmethod(name)

    def _request(self, name, params):
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

    def _dumbmethod(self, name):
        def foo(*args):
            return self._request(name, args)
        return foo

#r = Remote("http://localhost:8080/api")
#r.hello("JsonApp")
