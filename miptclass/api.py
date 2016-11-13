#   encoding: utf8
#   api.py

import logging

from json import dump, dumps
from pprint import pprint
from time import time, sleep
from itertools import islice
from requests import Session, codes


class VkRequestRoutine(object):

    VK_API_VERSION = '5.53'
    REQUEST_RATE = 0.433
    REQUEST_DELAY = 1.500

    def __init__(self, session=None, token=None, version=VK_API_VERSION):
        self.s = session if session else Session()
        self.v = version if version else VkRequestRoutine.VK_API_VERSION
        self.rate = 0.0
        self.token = token
        self.last_call = 0.0

    def request(self, url, payload, frame=0):
        if time() - self.last_call < VkRequestRoutine.REQUEST_RATE:
            sleep(VkRequestRoutine.REQUEST_RATE - (time() - self.last_call))

        self.last_call = time()
        self.rate = -time()

        r = self.s.post(url, data=payload)

        self.rate += time()
        logging.debug('request `%s`', r.url)
        logging.debug('url rate %s sec', self.rate)

        if r.status_code != codes.ok:
            pprint(r.content)
            return None

        content = r.json()

        if 'response' in content:
            return content['response']

        if content['error']['error_code'] == 6:  # Too many requests per second
            logging.debug('%d Too many requests per second: waiting %f seconds',
                        frame, VkRequestRoutine.REQUEST_DELAY)
            sleep(VkRequestRoutine.REQUEST_DELAY)
            logging.debug('%d Try recursively execute request', frame)
            return self.request(url, payload, frame + 1)

        logging.error('request error: %r', content['error'])

        return content['error']


class Groups(VkRequestRoutine):

    URI = 'https://api.vk.com/method/groups.{0}'

    def __init__(self, session=None, token=None, version=None):
        super(Groups, self).__init__(session, token, version)

    def getAllMembers(self, gid):
        members = self.getMembers(gid)
        offset = len(members['items'])

        while offset < members['count']:
            new_members = self.getMembers(gid, offset)
            members['items'].extend(new_members['items'])
            offset = len(members['items'])

        return members

    def getById(self, gids):
        URL = Groups.URI.format('getById')

        group_ids = gids if type(gids) == str else ','.join(str(x) for x in gids)

        payload = {
                'group_ids': group_ids,
                'fields': 'description,members_count,is_closed,counters',
                'v': self.v,
                'access_token': self.token,
                }

        return self.request(URL, payload)

    def getMembers(self, gid, offset=0, count=1000):
        URL = self.URI.format('getMembers')

        payload = {
            'group_id': gid,
            'offset': offset,
            'count': count,
            'fields': 'sex,photo_50,photo_100,photo_200_orig,photo_200,photo_400_orig,photo_max,photo_max_orig,universities',
            'v': self.v,
            'access_token': self.token,
        }

        return self.request(URL, payload)

    def get(self, user_id, extended=0, offset=0, count=1000):
        URL = self.URI.format('get')

        payload = {
            'user_id': user_id,
            'extended': extended,
            'offset': offset,
            'count': count,
            'access_token': self.token,
            'v': self.v,
        }

        return self.request(URL, payload)

    def getAllGroups(self, user_id, extended=0):
        groups = self.get(user_id)
        offset = len(groups['items'])

        while offset < groups['count']:
            new_groups = self.get(user_id, offset)
            groups['items'].extend(new_groups['items'])
            offset = len(groups['items'])

        return groups

    def dump(self, groups):
        if type(groups) != list and type(groups) != list:
            groups = [groups]

        for i, group in enumerate(groups):
            inf(i, 'name:         ', group['name'].encode('utf8'))
            inf(i, 'screen_name:  ', group['screen_name'].encode('utf8'))
            inf(i, 'group_id:     ', group['id'])
            inf(i, 'type:         ', group['type'].encode('utf8'))
            inf(i, 'members_count:', group['members_count'])


class Users(VkRequestRoutine):

    URI = 'https://api.vk.com/method/users.{0}'

    def __init__(self, session=None, token=None, version=None):
        super(Users, self).__init__(session, token, version)

    def get(self, uids, fields=None):
        URL = self.URI.format('get')

        fields = fields if fields is not None else \
        'sex,photo_50,photo_100,photo_200_orig,photo_200,photo_400_orig,photo_max,photo_max_orig,universities,schools,personal,books,movies,bdate,city,country,home_town'

        payload = {
            'user_ids': ','.join(str(x) for x in uids),
            'fields': fields,
            'v': self.v,
            'access_token': self.token,
        }
       
        return self.request(URL, payload)

    def getAllUsers(self, uids, fields=None):
        response = list()
        iterator = iter(uids)

        while True:
            chunk = list(islice(iterator, 1000))

            if not chunk:
                break

            response.extend(self.get(chunk, fields))

        return response


class Friends(VkRequestRoutine):

    URI = 'https://api.vk.com/method/friends.{0}'

    def __init__(self, session=None, token=None, version=None):
        super(Friends, self).__init__(session, token, version)

    def get(self, uid):
        URL = self.URI.format('get')

        payload = {
                'user_id': uid,
                'order': 'hints',
                'fields': 'nickname,domain',
                'v': self.v,
                'access_token': self.token,
                }

        return self.request(URL, payload)

    def getAll(self, uid):
        pass
