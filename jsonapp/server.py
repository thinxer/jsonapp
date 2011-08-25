def serve(app, host='127.0.0.1', port=8080):
    try:
        from paste import httpserver
        httpserver.serve(app, host=host, port=port)
        #from wsgiref.simple_server import make_server
        #make_server(host, port, self).serve_forever()
    except Exception, e:
        from google.appengine.ext.webapp.util import run_wsgi_app
        run_wsgi_app(app)
