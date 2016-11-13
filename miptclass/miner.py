#   encoding: utf8
#   miner.py

import logging

from copy import deepcopy
from itertools import zip_longest, tee
from functools import partial, reduce
from operator import itemgetter
from pprint import pprint
from requests import Session, codes
from time import time, sleep

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

    logging.log('start mining reference group brief info')
    reference  = ['miptru']
    mine_groups(reference, db, session, save)

    logging.log('build list of unique user identifiers')
    cursor = db.execute('SELECT id FROM users WHERE deactivated is NULL;')
    uids = map(itemgetter(0), cursor.fetchall())

    logging.log('start mining info about group members')
    mine_users(deepcopy(uids), db, session, save)

    logging.log('start mining friend lists of group members')
    mine_friends(uids, db, session, save)

def mine_groups(gids, db, session, save):
    groups = Groups(session=session, logging=True)
    response = groups.getById(gids)
    column_names = frozenset(dir(models.User))

    rows = (filter_fields(item, column_names) for item in response)
    rows = ((models.Group(**row), row['id']) for row in rows)
    rows, ids = zip(*rows)

    save(db, rows)

    logging.log('start mining group members')

    for group_id in ids:
        logging.log('process group #', group_id)
        mine_group(group_id, db, session, save)

def mine_group(gid, db, session, save):
    groups = Groups(session=session, logging=True)
    response = groups.getAllMembers(gid)
    column_names = frozenset(dir(models.User))
    rows = [models.User(**filter_fields(item, column_names)) for item in response['items']]

    save(db, rows)

def mine_users(uids, db, session, save):
    users = Users(session=session, logging=True)
    response = users.getAllUsers(uids)
    user_columns = frozenset(dir(models.User))
    university_columns = frozenset(dir(models.University))
    user_university_columns = frozenset(dir(models.UserUniversities))

    save(db, (models.User(**filter_fields(item, user_columns)) for item in response))

    universities = filter(lambda x: 'universities' in x, response)
    universities = map(itemgetter('id', 'universities'), universities)
    universities, user_university = tee(universities)
    universities = reduce(lambda x, y: x + y[1], universities, [])
    universities = (models.University(**filter_fields(item, university_columns)) for item in universities)

    save(db, universities)

    user_university = map(lambda x: zip_longest((x[0],), map(itemgetter('id'), x[1]), fillvalue=x[0]), user_university)
    user_university = reduce(lambda x, y: x + list(y), user_university, [])
    user_university = map(lambda x: dict(id=x[0], university_id=x[1]), user_university)
    user_university = (models.UserUniversity(**filter_fields(item, user_university_columns)) for item in user_university)

    save(db, universities)

def mine_friends(uids, db, session, save):
    friends = Friends(session=session, logging=logging)
    friend_columns = frozenset(dir(models.UserFriends))

    for i, uid in enumerate(uids):
        if i % 100 == 0:
            logging.log('processing user #', i)

        response = friends.get(uid)
        user_friends = (filter_fields(row, friend_columns) for row in response['items'])
        user_friends = (models.UserFriends(id=uid, friend_id=row['id']) for row in user_friends)

        db.add_all(user_friends)
        db.commit()
