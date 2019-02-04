import re
import os
import json
import logging
import time
import urllib.parse
import webbrowser

import requests


__all__ = ['FitbitClient']


log = logging.getLogger(__name__)


class FitbitClient(object):
    def __init__(self, access_token):
        self.access_token = access_token
        self.session = requests.Session()
        self.session.timeout = 30
        self.session.headers['Authorization'] = 'Bearer ' + access_token
        self.profile = self.get_profile()

    @property
    def user_id(self):
        return self.profile['encodedId']

    def get_profile(self):
        r = self.session.get('https://api.fitbit.com/1/user/-/profile.json')
        r.raise_for_status()
        return json.loads(r.text)['user']

    def get_sleep(self, date):
        r = self.session.get('https://api.fitbit.com/1.2/user/{}/sleep/date/{}.json'
            .format(self.user_id, str(date)))
        r.raise_for_status()
        return json.loads(r.text)['sleep']

    def get_sleep_range(self, date_start, date_end):
        r = self.session.get('https://api.fitbit.com/1.2/user/{}/sleep/date/{}/{}.json'
            .format(self.user_id, str(date_start), str(date_end)))
        r.raise_for_status()
        return json.loads(r.text)['sleep']

    def get_heartrate_range(self, date_start, date_end):
        r = self.session.get('https://api.fitbit.com/1/user/-/activities/heart/date/{}/{}.json'
            .format(str(date_start), str(date_end)))
        r.raise_for_status()
        return json.loads(r.text)['activities-heart']

    def get_heartrate_intraday(self, date):
        r = self.session.get('https://api.fitbit.com/1/user/-/activities/heart/date/{}/{}/1min.json'
            .format(str(date), str(date)))
        r.raise_for_status()
        return json.loads(r.text)['activities-heart-intraday']['dataset']

    def get_activities(self, date):
        r = self.session.get('https://api.fitbit.com/1/user/-/activities/date/{}.json'
            .format(str(date)))
        r.raise_for_status()
        return json.loads(r.text)

    def get_steps(self):
        raise NotImplementedError
