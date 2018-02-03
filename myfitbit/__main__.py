import argparse
import configparser
import getpass
import logging
import json

import requests

from . import Fitbit, FitbitAuth
from .export import FitbitExport

logging.basicConfig(level=logging.DEBUG)

def main():
    config = configparser.ConfigParser()
    config.read('config.ini')

    fa = FitbitAuth(
        client_id=config['fitbit_auth']['client_id'],
        client_secret=config['fitbit_auth']['client_secret'],
    )
    fa.ensure_access_token()

    try:
        f = Fitbit(access_token=fa.access_token['access_token'])
        print(json.dumps(f.profile, indent=2))
    except requests.exceptions.HTTPError as e:
        print(e.response.status_code)
        if e.response.status_code == 429:
            print(e.response.headers)
            return
        raise

    export = FitbitExport('.', f)

    export.sync_sleep()
    export.sync_heartrate_intraday()


if __name__ == '__main__':
    main()
