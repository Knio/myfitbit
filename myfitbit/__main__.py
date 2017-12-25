from datetime import date
import argparse
import configparser
import getpass
import logging
import json

logging.basicConfig(level=logging.DEBUG)

from . import Fitbit, FitbitAuth


def main():
    config = configparser.ConfigParser()
    config.read('config.ini')

    fa = FitbitAuth(
        client_id=config['fitbit_auth']['client_id'],
        client_secret=config['fitbit_auth']['client_secret'],
    )
    fa.ensure_access_token()

    f = Fitbit(access_token=fa.access_token['access_token'])
    print(json.dumps(f.profile, indent=2))

    sleep = f.get_sleep(date(2017, 4, 8))
    print(json.dumps(sleep, indent=2))



if __name__ == '__main__':
    main()
    # parser = argparse.ArgumentParser()
    # parser.add_argument('--username', required=True)
    # parser.add_argument('--ask-password', required=True, action='store_true')
    # args = parser.parse_args()
