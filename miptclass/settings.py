#   encoding: utf8
#   settings.py

DATABASE_URI = 'sqlite:///mipt-classifier.db'

DEBUG = True
PROFILE = False

CLIENT_ID = None  # Vk app dd
CLIENT_SECRET = ''  # Vk app secret

REDIRECT_URI = 'http://example.com/mipt-classifier'

URL_PREFIX = ''

VK_API_VERSION = '5.53'

try:
    from miptclass_settings import *
except ImportError:
    pass
