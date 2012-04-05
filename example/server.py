'''
A Demo Server for JsonApp.

Run 'python server.py' and point your browser at 'http://localhost:8080'.

    {"hello":"JsonApp"}

That's it.
'''
from jsonapp import DefaultWebApplication, serve

application = DefaultWebApplication()
api = application.jsonapp.decorator()

@api
def hello(name):
    return { "hello":name }

serve(application, "127.0.0.1", 8080)
