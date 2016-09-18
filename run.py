#!/usr/bin/env python3
#   encoding: utf8
#   run.py

from miptclass import settings
from miptclass.wsgi import app

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=settings.DEBUG)
