from datetime import date
import argparse
import getpass
import json

from . import Fitbit

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--username', required=True)
    parser.add_argument('--ask-password', required=True, action='store_true')
    args = parser.parse_args()

    if args.ask_password:
        password = getpass.getpass('Password for {}: '.format(args.username))

    f = Fitbit()
    r = f.login(username=args.username, password=password)

    user_info = f.user_info
    print(json.dumps(user_info, indent=2))


    sleep = f.get_sleep(date(2017, 4, 8))
    print(json.dumps(sleep, indent=2))

