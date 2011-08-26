from setuptools import setup

setup(
    name = "jsonapp",
    version = "0.0.2",
    author = "Jianfei Wang",
    author_email = "me@thinxer.com",
    description = "A simple framework for pure-ajax applications.",
    url = "https://github.com/thinxer/jsonapp",
    license = "MIT",
    keywords = "json wsgi webapp",
    packages = ['jsonapp'],
    package_data = {'jsonapp': ['*.js']},
)
