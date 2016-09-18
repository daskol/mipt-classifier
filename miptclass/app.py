#   encoding: utf8
#   app.py

from flask import Flask

app = Flask(__name__)
app.config.from_object('miptclass.settings')