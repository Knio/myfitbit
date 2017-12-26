from datetime import date, timedelta
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

    sleep = []
    start = date(2017, 1, 1)
    dt = timedelta(days=90)
    while 1:
        n = start + dt
        s = f.get_sleep_range(start, n)
        sleep.extend(s)
        start = n
        if n > date.today():
            break

    with open('sleep.json', 'w') as f:
        f.write(json.dumps(sleep, indent=2))
    # print(json.dumps(sleep, indent=2))



if __name__ == '__main__':
    main()
    # parser = argparse.ArgumentParser()
    # parser.add_argument('--username', required=True)
    # parser.add_argument('--ask-password', required=True, action='store_true')
    # args = parser.parse_args()
