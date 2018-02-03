from ._version import __version__, version

import base64
import re
import os
import json
import logging
import time
import urllib.parse
import webbrowser

import requests
import http.server

__all__ = ['Fitbit', 'FitbitAuth']

log = logging.getLogger(__name__)

class RedirectServer(object):
    IP = '127.0.0.1'
    PORT = 8189
    URL = 'http://localhost:{}/auth_code'.format(PORT)
    def __init__(self):
        self.result = None
        class HTTPHandler(http.server.BaseHTTPRequestHandler):
            def do_GET(handler):
                url = urllib.parse.urlparse(handler.path)
                if url.path != '/auth_code':
                    # browser may want favicon.ico, etc
                    handler.send_response(404)
                    handler.end_headers()
                    handler.wfile(b'')
                query = urllib.parse.parse_qs(url.query)
                self.result = query
                handler.send_response(200)
                handler.send_header('Content-type', 'text/html')
                handler.end_headers()
                handler.wfile.write(b'OK<script>window.close();</script>')
        self.handler_class = HTTPHandler

    def get_result(self):
        httpd = http.server.HTTPServer(('127.0.0.1', self.PORT), self.handler_class)
        httpd.timeout = 5
        for i in range(5):
            httpd.handle_request()
            if self.result:
                return self.result
        raise RuntimeError('Failed to auth with browser')


class FitbitAuth(object):
    ACCESS_TOKEN_FILE = '.myfitbit_access_token'
    def __init__(self, client_id, client_secret):
        self.client_id = client_id
        self.client_secret = client_secret
        self.access_token = None

    def get_auth_code(self):
        log.info('Getting new auth code')
        url = 'https://www.fitbit.com/oauth2/authorize?' + \
            '&'.join('{}={}'.format(k, v) for k, v in {
                'response_type': 'code',
                'client_id': self.client_id,
                'redirect_uri': RedirectServer.URL,
                'scope': '%20'.join(('activity', 'heartrate', 'location', 'nutrition', 'profile', 'settings', 'sleep', 'social', 'weight')),
                'expires_in': '31536000',
            }.items())

        redirect = RedirectServer()
        webbrowser.open_new(url)
        result = redirect.get_result()
        return result['code'][0]

    def get_access_token(self):
        log.info('Getting new access token')
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
        now = int(time.time())
        if os.path.isfile(self.ACCESS_TOKEN_FILE):
            access_token = json.load(open(self.ACCESS_TOKEN_FILE))
            if now > access_token['time'] + access_token['expires_in']:
                log.info('Cached access token is expired')
                os.unlink(self.ACCESS_TOKEN_FILE)
            else:
                self.access_token = access_token
                return
        self.access_token = self.get_access_token()
        self.access_token['time'] = now
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
