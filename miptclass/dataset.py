#!/usr/bin/env python3
#   encoding: utf8
#   dataset.py

import logging

from itertools import count
from miptclass import models
from miptclass.settings import ML_DATASET, ML_FRIEND_ENCODER
from numpy import zeros
from operator import itemgetter
from os.path import realpath
from scipy.io import savemat
from scipy.sparse import csr_matrix, lil_matrix
from sklearn.externals.joblib import dump
from sklearn.preprocessing import LabelBinarizer
from tqdm import tqdm


def make_features_from_friend_list(friend_ids, freq_friends):
    feat = zeros(len(freq_friends), dtype=int)

    for friend_id in friend_ids:
        idx = freq_friends.get(friend_id, None)

        if idx is not None:
            feat[idx] = True

    return feat

def make_dataset(db, filename, friend_enc_file):
    logging.info('start making dataset')

    cursor = db.execute("""
        SELECT
            id
        FROM universities
        WHERE name LIKE '%МФТИ%';
        """)
    mipt_ids = frozenset(map(itemgetter('id'), cursor.fetchall()))
    logging.info('MIPT university ids: %r', mipt_ids)

    logging.info('build the most frequent friends')
    cursor = db.execute("""
        SELECT
            friend_id
        FROM user_friends
        GROUP BY friend_id
        HAVING COUNT(friend_id) > 4;
        """)
    freq_friend_ids = map(itemgetter('friend_id'), cursor.fetchall())

    logging.info('build and store friend encoder into `%s`', friend_enc_file)
    friend_encoder = LabelBinarizer(sparse_output=True)
    friend_encoder.fit(tuple(freq_friend_ids))
    friend_encoder_size = friend_encoder.classes_.shape[0]

    with open(friend_enc_file, 'wb') as fout:
        dump(friend_encoder, fout)

    logging.info('total %d the most frequent friends', friend_encoder_size)

    uid_count = db.execute("""
        SELECT
            COUNT(u.id) AS cnt
        FROM user_universities uu
        JOIN users u ON u.id = uu.id;
        """).fetchone()['cnt']

    cursor = db.execute("""
        SELECT
            u.id AS id
        FROM user_universities uu
        JOIN users u ON u.id = uu.id;
        """)
    uids = map(itemgetter('id'), cursor.fetchall())
    dataset = lil_matrix((uid_count, 1 + 1 + friend_encoder_size), dtype=int)

    for i, uid in enumerate(tqdm(uids, total=uid_count, unit='uid')):
        cursor = db.execute("""
            SELECT
                university_id
            FROM user_universities
            WHERE id = :uid;
            """, dict(uid=uid))
        university_ids = map(itemgetter('university_id'), cursor.fetchall())
        is_mipt = any([university_id in mipt_ids
                       for university_id in university_ids])

        row = zeros(1 + 1 + friend_encoder_size, dtype=int)
        row[0] = uid
        row[1] = is_mipt

        cursor = db.execute("""
            SELECT
                friend_id
            FROM user_friends
            WHERE id = :uid;
            """, dict(uid=uid))
        friend_ids = map(itemgetter('friend_id'), cursor.fetchall())
        friend_ids = list(friend_ids)

        if friend_ids:
            row[2:] = friend_encoder.transform(friend_ids).sum(axis=0)

        dataset[i, :] = row

    logging.info('total %d non zero elements', dataset.nnz)
    logging.info('converting lil to csr format')

    dataset = csr_matrix(dataset)
    filename = realpath(filename)

    logging.info('store dataset matrix into `%s`', filename)

    with open(filename, 'wb') as fout:
        savemat(fout, dict(dataset=dataset.T))

    logging.info('done')

    return dataset

def test():
    logging.basicConfig(
            format='%(asctime)s : %(levelname)s : %(message)s',
            level=logging.INFO)

    dataset = make_dataset(models.db, ML_DATASET, ML_FRIEND_ENCODER)


if __name__ == '__main__':
    test()
