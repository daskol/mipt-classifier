#   encoding: utf8
#   wsgi.py

from miptclass import cli, blueprints
from miptclass.app import app


cli.init_app(app)
blueprints.init_app(app)

if app.config.get('PROFILE', False):
    from werkzeug.contrib.profiler import ProfilerMiddleware
    app.wsgi_app = ProfilerMiddleware(app.wsgi_app, restrictions=[], profile_dir='/tmp')
