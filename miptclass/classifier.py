#   encoding: utf8
#   classifier.py

from miptclass.settings import ML_BASELINE, ML_FRIEND_ENCODER
from sklearn.externals.joblib import load


def init_app(app):
    app.classifier = BaselineClassifier()


class BaselineClassifier(object):

    def __init__(self, preload=False):
        self.clf = None
        self.enc = None

        if preload:
            self.__load()

    def __call__(self, friend_list):
        if not self.clf or not self.enc:
            self.__load()

        return self.__classify(friend_list)

    def __classify(self, friend_list):
        friends = self.enc.transform(friend_list).sum(axis=0)
        result = self.clf.predict(friends)[0]
        return bool(result == 1)

    def __load(self):
        self.enc = load(ML_FRIEND_ENCODER)
        self.clf = load(ML_BASELINE)
