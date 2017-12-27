from ._version import __version__, version

import base64
import re
import os
import json
import webbrowser
import urllib.parse

import requests
from bs4 import BeautifulSoup
import http.server

__all__ = ['Fitbit', 'FitbitAuth']


class RedirectServer(object):
    IP = '127.0.0.1'
    PORT = 8189
    URL = 'http://localhost:{}/'.format(PORT)
    def __init__(self):
        self.result = None
        class HTTPHandler(http.server.BaseHTTPRequestHandler):
          def do_GET(s):
                url = urllib.parse.urlparse(s.path)
                query = urllib.parse.parse_qs(url.query)
                self.result = query
                s.send_response(200)
                s.send_header('Content-type', 'text/html')
                s.end_headers()
                s.wfile.write(b'OK<script>window.close();</script>')
        self.handler_class = HTTPHandler

    def get_result(self):
        httpd = http.server.HTTPServer(('127.0.0.1', self.PORT), self.handler_class)
        httpd.timeout = 30
        httpd.handle_request()
        if not self.result:
            raise RuntimeError('Failed to auth with browser')
        return self.result


class FitbitAuth(object):
    ACCESS_TOKEN_FILE = '.myfitbit_access_token'
    def __init__(self, client_id, client_secret):
        self.client_id = client_id
        self.client_secret = client_secret
        self.access_token = None

    def get_auth_code(self):
        url = 'https://www.fitbit.com/oauth2/authorize?' + \
            '&'.join('{}={}'.format(k, v) for k, v in {
                'response_type': 'code',
                'client_id': self.client_id,
                'redirect_uri': RedirectServer.URL,
                'scope': '%20'.join(('activity', 'heartrate', 'location', 'nutrition', 'profile', 'settings', 'sleep', 'social', 'weight')),
                'expires_in': '31536000',
            }.items())

        webbrowser.open_new(url)
        r = RedirectServer().get_result()
        return r['code'][0]

    def get_access_token(self):
        auth_code = self.get_auth_code()
        auth_string = base64.b64encode(
            self.client_id.encode('ascii') + b':' + self.client_secret.encode('ascii')).decode('ascii')
        r = requests.post('https://api.fitbit.com/oauth2/token',
                headers={
                    'Authorization': 'Basic ' + auth_string,
                },
                data={
                    'clientId': self.client_id,
                    'code': auth_code,
                    'grant_type': 'authorization_code',
                    'redirect_uri': RedirectServer.URL,
                },
                timeout=30
        )
        r.raise_for_status()
        return json.loads(r.text)

    def ensure_access_token(self):
        if self.access_token:
            return
        if os.path.isfile(self.ACCESS_TOKEN_FILE):
            self.access_token = json.load(open(self.ACCESS_TOKEN_FILE))
            return
        self.get_auth_code()
        self.access_token = self.get_access_token()
        with open(self.ACCESS_TOKEN_FILE, 'w') as f:
            json.dump(self.access_token, f, sort_keys=True, indent=2)


class Fitbit(object):
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

    def get_heartrate_intraday(self, date):
        r = self.session.get('https://api.fitbit.com/1/user/-/activities/heart/date/{}/{}/1min.json'
            .format(
                str(date),
                str(date)
            )
        )
        r.raise_for_status()
        return json.loads(r.text)['activities-heart-intraday']['dataset']

    def get_steps(self):
        raise NotImplementedError
