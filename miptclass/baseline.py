#   encoding: utf8
#   baseline.py

import logging

from miptclass.settings import ML_BASELINE, ML_DATASET, ML_SEED
from numpy import array, nonzero
from os.path import realpath
from scipy.io import loadmat
from sklearn.externals.joblib import dump
from sklearn.metrics import accuracy_score, classification_report
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB


logging.basicConfig(
        format='%(asctime)s : %(levelname)s : %(message)s',
        level=logging.INFO)

logging.info('loading and preparing datasets')
dataset = loadmat(ML_DATASET)['dataset'].T

target = array(dataset[:, 1].todense()).reshape(-1)
data = dataset[:, 2:]

X_train, X_test, y_train, y_test = train_test_split(
    data, target,
    random_state=ML_SEED, test_size=0.20)

logging.info('fit model')
clf = MultinomialNB()
clf.fit(X_train, y_train)

logging.info('evaluate model')
score = accuracy_score(y_test, clf.predict(X_test))
report = classification_report(y_test, clf.predict(X_test))

logging.info('BRIEF REPORT')

for line in report.splitlines():
    logging.info(line)

logging.info('acccuracy of classification is %f', score)

filename = realpath(ML_BASELINE)
logging.info('store model into `%s`', filename)
dump(clf, filename)

logging.info('done')
