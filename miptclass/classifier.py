#   encoding: utf8
#   classifier.py

from sklearn.externals.joblib import load


FRIEND_ENCODER_FILENAME = 'var/models/friend-encoder.pkl'
MODEL_BASELINE_PATH = 'var/models/baseline.pkl'


def init_app(app):
    app.classifier = BaselineClassifier()


class BaselineClassifier(object):

    def __init__(self, preload=False):
        self.clf = None
        self.enc = None

        if preload:
            self.__load()

    def __call__(self, friend_list):
        if not self.clf or not self.env:
            self.__load()

        return self.__classify(friend_list)

    def __classify(self, friend_list):
        friends = self.enc.transform(friend_list).sum(axis=0)
        result = self.clf.predict(friends)[0]
        return bool(result == 1)

    def __load(self):
        self.enc = load(FRIEND_ENCODER_FILENAME)
        self.clf = load(MODEL_BASELINE_PATH)
