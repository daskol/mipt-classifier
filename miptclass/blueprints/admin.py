#   encoding: utf8
#   admin.py

import logging

from flask import Blueprint, current_app, render_template
from miptclass import settings, models


logger = logging.getLogger(__name__)
bp = Blueprint('admin', __name__)


@bp.route('/', methods=['GET'])
def index():
    url = 'https://oauth.vk.com/authorize?client_id={0}&redirect_uri={1}&display={2}&scope={3}&response_type=code&v=5.53'.format(
            settings.CLIENT_ID,
            settings.REDIRECT_URI,
            'page',
            'friends'
    )

    stat = dict()

    cursor = models.db.execute('SELECT COUNT(*) FROM users;')
    stat['num_users'] = cursor.fetchone()[0]

    cursor = models.db.execute('SELECT COUNT(*) FROM user_friends;')
    stat['num_friends'] = cursor.fetchone()[0]

    cursor = models.db.execute('SELECT COUNT(*) FROM groups;')
    stat['num_groups'] = cursor.fetchone()[0]

    cursor = models.db.execute('SELECT COUNT(*) FROM access_tokens;')
    stat['num_tokens'] = cursor.fetchone()[0]

    cursor = models.db.execute('SELECT id, token, expires_in FROM access_tokens WHERE valid = 1;')
    tokens = cursor.fetchall()

    return render_template('admin/index.html', action=url, stat=stat, tokens=tokens)
