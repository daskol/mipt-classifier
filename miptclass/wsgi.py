#   encoding: utf8
#   wsgi.py

from miptclass import cli, blueprints, classifier
from miptclass.app import app
from miptclass.models import db


blueprints.init_app(app)
cli.init_app(app)
classifier.init_app(app)

app.db = db

if app.config.get('PROFILE', False):
    from werkzeug.contrib.profiler import ProfilerMiddleware
    app.wsgi_app = ProfilerMiddleware(app.wsgi_app, restrictions=[], profile_dir='/tmp')
