import base64
import http.server
import json
import logging
import os
import time

import requests


__all__ = ['FitbitAuth']

log = logging.getLogger(__name__)


class RedirectServer(object):
    IP = '127.0.0.1'
    PORT = 18189
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
    def __init__(self, client_id, client_secret, access_token_file=None):
        self.client_id = client_id
        self.client_secret = client_secret
        self.access_token_file = access_token_file
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

    def get_access_token_refresh(self, refresh_token):
        log.info('Refreshing access token')
        auth_string = base64.b64encode(
            self.client_id.encode('ascii') + b':' + self.client_secret.encode('ascii')).decode('ascii')
        r = requests.post('https://api.fitbit.com/oauth2/token',
                headers={
                    'Authorization': 'Basic ' + auth_string,
                },
                data={
                    'grant_type': 'refresh_token',
                    'refresh_token': refresh_token,
                },
                timeout=30
        )
        r.raise_for_status()
        return json.loads(r.text)

    def ensure_access_token(self):
        access_token = self.access_token
        if not access_token:
            if os.path.isfile(self.access_token_file):
                access_token = json.load(open(self.access_token_file))
            else:
                access_token = self.get_access_token()

        now = int(time.time())
        if now > access_token['time'] + access_token['expires_in'] - 30:
            log.info('Access token is expired')
            access_token = self.get_access_token_refresh(access_token['refresh_token'])

        if self.access_token is not access_token:
            access_token['time'] = now
            with open(self.access_token_file, 'w') as f:
                json.dump(access_token, f, sort_keys=True, indent=2)
            self.access_token = access_token

        return access_token['access_token']

