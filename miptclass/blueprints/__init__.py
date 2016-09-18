#   encoding: utf8
#   __init__.py

from miptclass import settings
from miptclass.blueprints import admin, api

def init_app(app):
    app.register_blueprint(admin.bp, url_prefix=settings.URL_PREFIX + '/admin')
    app.register_blueprint(api.bp, url_prefix=settings.URL_PREFIX + '/api')
