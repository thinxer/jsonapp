A KISS WSGI application built to make pure AJAX application easier.

Example server code:

    # server.py
    from jsonapp import DefaultWebApplication, serve

    application = DefaultWebApplication()
    api = application.jsonapp.decorator()

    @api
    def hello(name):
        return { "hello":name }

    serve(application, "127.0.0.1", 8080)

Example JavaScript client code:

    // include the script '/_client.js' first.
    var r = new JsonRemote("/api");
    r.call("hello", ["JsonApp"], function(err, d) {
        if (err) {
            document.write(JSON.stringify(err));
        } else {
            document.write(JSON.stringify(d));
        }
    });

Example Python client code:

    from jsonapp import Remote
    r = Remote('http://localhost:8080/api')
    r.hello('world')

The ``r`` object is tab-completable in IPython, which is quite handy.

The entire framework is designed to be easy to use, and no easier.
To speed up development, it also comes with a static file server. Drop your
static files into ``static`` directory and your app is up and running.
``index.html`` will be automatically mapped to the root path ``/``.
