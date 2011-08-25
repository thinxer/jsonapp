class Redirector(object):
    def __init__(self, target_path, target_app):
        self.target_path = target_path
        self.target_app = target_app

    def __call__(self, env, start_response):
        env['PATH_INFO'] = self.target_path
        return self.target_app(env, start_response)
