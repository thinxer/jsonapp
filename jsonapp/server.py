def serve(app, host='127.0.0.1', port=8080):
    from wsgiref.simple_server import make_server
    make_server(host, port, app).serve_forever()
