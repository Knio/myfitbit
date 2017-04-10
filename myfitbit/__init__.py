from ._version import __version__, version

import re
import json

import requests
from bs4 import BeautifulSoup

__all__ = ['Fitbit']

LOGIN_URL = 'https://www.fitbit.com/login'

class Fitbit(object):
    def __init__(self):
        self.session = requests.Session()
        self.user_info = None

    @property
    def user_id(self):
        return self.user_info['encodedId']

    @property
    def api_url(self):
        return 'https://{}'.format(self.user_info['apiUrl'])

    @property
    def authorization(self):
        return self.user_info['oauth2Token']

    def login(self, username, password):
        req = self.session.get(LOGIN_URL, headers={'Referer': LOGIN_URL})
        login_page = BeautifulSoup(req.text, 'html.parser')

        source_page = \
            login_page.find('input', {'name':'_sourcePage'}).get('value')

        fp = \
            login_page.find('input', {'name':'__fp'}).get('value')

        login_data = {
            'login': 'Log+In',
            'includeWorkflow': '',
            'redirect': '',
            'switchToNonSecureOnRedirect': '',
            'disableThirdPartyLogin': 'false',
            'email': username,
            'password': password,
            'rememberMe': 'true',
            '_sourcePage': source_page,
            '__fp': fp,
        }

        req = self.session.post(LOGIN_URL, data=login_data, headers={'Referer': LOGIN_URL})

        dashboard = BeautifulSoup(req.text, 'html.parser')

        user_script = \
            dashboard.find('div', {'id':'dash'}).next_element.next_element.text

        user_json = re.match(r'^[^{]*(\{.*\})[^}]*$', user_script).group(1)
        self.user_info = json.loads(user_json)


    def get_sleep(self, date):
        req = self.session.get(
            '{api_url}/1.2/user/{user_id}/sleep/date/{date}.json?date={date}&id={user_id}'.format(
                api_url=self.api_url,
                user_id=self.user_id,
                date=str(date),
            ),
            headers={
                'Referer': 'https://www.fitbit.com/sleep',
                'Authorization': 'Bearer ' + self.authorization}
        )

        return req.json()

    def get_heartrate(self, date):
        raise NotImplementedError

        # https://www.fitbit.com/ajaxapi
        #
        # POST /ajaxapi HTTP/1.1
        # Host: www.fitbit.com
        # User-Agent: Mozilla/5.0 (Windows NT 10.0; WOW64; rv:52.0) Gecko/20100101 Firefox/52.0
        # Accept: */*
        # Accept-Language: en-US,en;q=0.5
        # Accept-Encoding: gzip, deflate, br
        # Content-Type: application/x-www-form-urlencoded; charset=UTF-8
        # X-Requested-With: XMLHttpRequest
        # Referer: https://www.fitbit.com/2017/04/09

        # request={"template":"/ajaxTemplate.jsp","serviceCalls":[{"name":"activityTileData","args":{"date":"2017-04-08","dataTypes":"heart-rate"},"method":"getIntradayData"}]}
        # csrfToken=UUID



    def get_steps(self):
        raise NotImplementedError

    # https://web-api.fitbit.com/1/user/5M5DHS/activities/heart/date/2017-04-09/2017-04-02.json
    # https://web-api.fitbit.com/1/user/5M5DHS/activities/date/2017-04-09.json
    # https://web-api.fitbit.com/1.1/user/5M5DHS/sed/date/2017-04-09.json
    # https://web-api.fitbit.com/1.2/user/-/sleep/date/2017-04-09.json
