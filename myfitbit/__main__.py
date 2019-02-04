import argparse
import configparser
import getpass
import logging
import json

import requests

from . import FitbitClient, FitbitAuth
from . import FitbitDatastore, FitbitSync


def main():
    logging.basicConfig(level=logging.DEBUG)

    config = configparser.ConfigParser()
    config.read('myfitbit.ini')
    auth = config['fitbit_auth']

    fa = FitbitAuth(
        client_id=auth['client_id'],
        client_secret=auth['client_secret'],
        access_token_file=auth['access_token_file'] + '_' + auth['client_id']
    )
    access_token = fa.ensure_access_token()

    try:
        client = FitbitClient(access_token=access_token)
        logging.info(json.dumps(client.profile, indent=2))
        data = FitbitDatastore(client.user_id)
        FitbitSync(data, client).sync()

    except requests.exceptions.HTTPError as e:
        logging.info(e.response.status_code)
        if e.response.status_code == 429:
            logging.info(e.response.headers)
            # TODO sleep automatically here
            return
        raise



if __name__ == '__main__':
    main()
