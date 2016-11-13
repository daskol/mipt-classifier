#   encoding: utf8
#   miner.py

import logging

from itertools import zip_longest, tee
from functools import partial, reduce
from operator import itemgetter
from pprint import pprint
from requests import Session, codes
from time import time, sleep
from tqdm import tqdm

from miptclass import models
from miptclass.api import Groups, Users, Friends
from miptclass.models import User, Group, UserFriends


def filter_fields(row, column_names):
    return dict((field, value) for field, value in row.items() if field in column_names)

def save(db, rows):
    for row in rows:
        db.merge(row)
        db.commit()

def mine_reference_groups(db):
    session = Session()

    logging.info('start mining reference group brief info')
    reference  = ['miptru']
    mine_groups(reference, db, session, save)

    logging.info('build list of unique user identifiers')
    cursor = db.execute('SELECT id FROM users WHERE deactivated is NULL;')
    uids = tuple(map(itemgetter(0), cursor.fetchall()))

    logging.info('start mining info about group members')
    mine_users(uids, db, session, save)

    logging.info('start mining friend lists of group members')
    mine_friends(uids, db, session, save)

def mine_groups(gids, db, session, save):
    groups = Groups(session=session)
    response = groups.getById(gids)
    column_names = frozenset(dir(models.User))

    rows = (filter_fields(item, column_names) for item in response)
    rows = ((models.Group(**row), row['id']) for row in rows)
    rows, ids = zip(*rows)

    save(db, rows)

    logging.info('start mining group members')

    for group_id in ids:
        logging.info('process group #', group_id)
        mine_group(group_id, db, session, save)

def mine_group(gid, db, session, save):
    groups = Groups(session=session)
    response = groups.getAllMembers(gid)
    column_names = frozenset(dir(models.User))
    rows = [models.User(**filter_fields(item, column_names))
            for item in response['items']]

    save(db, rows)

def mine_users(uids, db, session, save):
    user_columns = frozenset(dir(models.User))
    university_columns = frozenset(dir(models.University))
    user_university_columns = frozenset(dir(models.UserUniversities))

    logging.info('insert user profiles into database')
    users = Users(session=session)
    response = users.getAllUsers(uids)

    save(db, (models.User(**filter_fields(item, user_columns))
              for item in response))

    logging.info('insert universities into datatabase')

    universities = filter(lambda x: 'universities' in x, response)
    universities = map(itemgetter('id', 'universities'), universities)
    universities, user_university = tee(universities)
    universities = reduce(lambda x, y: x + y[1], universities, [])
    universities = (models.University(**filter_fields(item,
                                                      university_columns))
                    for item in universities)

    save(db, universities)

    logging.info('insert user\'s universities into database')

    user_university = map(lambda x:
                          zip_longest((x[0],),
                                      map(itemgetter('id'), x[1]),
                                      fillvalue=x[0]),
                          user_university)
    user_university = reduce(lambda x, y: x + list(y), user_university, [])
    user_university = map(lambda x: dict(id=x[0], university_id=x[1]),
                          user_university)
    user_university = (models.UserUniversities(**filter_fields(item,
                                               user_university_columns))
                       for item in user_university)

    user_university = list(user_university)

    save(db, user_university)

def mine_friends(uids, db, session, save):
    friends = Friends(session=session)
    friend_columns = frozenset(dir(models.UserFriends))

    for i, uid in enumerate(tqdm(uids, unit='uid')):
        response = friends.get(uid)

        if all((response.get('error_code') == 15,
                response.get('error_msg') == 'Access denied: user deactivated')):

            db.execute("""
                UPDATE users
                SET deactivated = 'deactivated';
                """)
            db.commit()
        elif 'error_code' in response:
            logging.error('error was revieved for uid %d: %s(%d)',
                    uid, response['error_code'], response['error_msg'])
        else:
            user_friends = (filter_fields(row, friend_columns)
                            for row in response['items'])
            user_friends = (models.UserFriends(id=uid, friend_id=row['id'])
                            for row in user_friends)

            db.add_all(user_friends)
            db.commit()
