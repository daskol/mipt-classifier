#   encoding: utf8
#   common.py

from __future__ import print_function
from datetime import datetime

#
#   Debug functions

def debug_message(prefix):
    def wrapper(*args, **kwargs):
        print(prefix(), *args, **kwargs)
    return wrapper

@debug_message
def inf(*args, **kwargs):
    return '\x1b[32m[INF]\x1b[0m' + ' ' + timestamp()

@debug_message
def log(*args, **kwargs):
    return '\x1b[33m[LOG]\x1b[0m' + ' ' + timestamp()

@debug_message
def err(*args, **kwargs):
    return '\x1b[31m[ERR]\x1b[0m' + ' ' + timestamp()

def stub(*args, **kwargs):
    pass

def timestamp():
    return '\x1b[35m{}\x1b[0m'.format(datetime.now().time().isoformat())
