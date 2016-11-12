#   encoding: utf8
#   api.py

import logging

from datetime import datetime, timedelta
from flask import Blueprint, current_app, jsonify, request, redirect, url_for
from requests import Session

from miptclass import settings, models
from miptclass.blueprints import admin
from miptclass.models import AccessToken


logger = logging.getLogger(__name__)
bp = Blueprint('api', __name__)


@bp.route('/access_token', methods=['GET'])
def index():
    if 'code' not in request.args:
        return jsonify(error=request.args.get('error'), error_description=request.args.get('error_description')), 400

    session = Session()
    response = session.get('https://oauth.vk.com/access_token', params=dict(
        client_id=settings.CLIENT_ID,
        client_secret=settings.CLIENT_SECRET,
        redirect_uri='http://139.59.159.51/mipt-classifier/api/access_token',
        code=request.args['code']
        ))

    if response.status_code != 200:
        return jsonify(), 400

    json = response.json()
    expires_in = datetime.now() + timedelta(seconds=json['expires_in'])
    token = AccessToken(id=json['user_id'], token=json['access_token'], expires_in=expires_in)

    models.db.merge(token)
    models.db.commit()

    return redirect(url_for('admin.index'))