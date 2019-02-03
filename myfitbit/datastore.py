
import os
import json
import logging
from datetime import date, time, timedelta

log = logging.getLogger(__name__)

class FitbitDatastore(object):
    '''
    Local data store of Fitbit json objects.
    '''
    # TODO store profile
    def __init__(self, root, client=None, user_id=None):
        self.root = os.path.abspath(root)
        self.client = client
        self.user_id = user_id

    def filename(self, *args):
        u = self.client and self.client.user_id or self.user_id
        return os.path.join(self.root, u, *args)

    @staticmethod
    def write(filename, data):
        dirname = os.path.dirname(filename)
        os.makedirs(dirname, exist_ok=True)
        with open(filename, 'w') as f:
            f.write(json.dumps(data, indent=2, sort_keys=True))

    def sync_ranged_data(self, name, client_fn):
        '''
        Downloads date-range time series data from
        the FitBit API to the local data store.
        '''
        month = 2015 * 12 # TODO use profile['memberSince']
        while 1:
            date_start = date(month // 12, month % 12 + 1, 1)
            month += 1
            date_end =   date(month // 12, month % 12 + 1, 1)

            if date_start > date.today():
                break

            partial = date_end > date.today()
            partial_filename = self.filename(name, '{}.{:04d}.{:02d}.partial.json'.format(
                name,
                date_start.year,
                date_start.month,
            ))
            filename = self.filename(name, '{}.{:04d}.{:02}.json'.format(
                name,
                date_start.year,
                date_start.month,
            ))

            if os.path.isfile(partial_filename):
                os.remove(partial_filename)

            if partial:
                filename = partial_filename
            elif os.path.isfile(filename):
                log.info('Cached: %s', filename)
                continue

            log.info('Downloading: %s', filename)
            data = client_fn(
                date_start,
                date_end - timedelta(days=1)
            )
            self.write(filename, data)

    def sync_sleep(self):
        '''
        Downloads sleep data from the FitBit API to the local data store
        '''
        self.sync_ranged_data('sleep', self.client.get_sleep_range)

    def sync_heartrate(self):
        '''
        Downloads heartrate data from the FitBit API to the local data store
        '''
        self.sync_ranged_data('heartrate', self.client.get_heartrate_range)

    def day_filenames(self, name):
        # TODO use profile['memberSince']
        start = date(2017, 1, 1)
        days = 0
        while 1:
            d = start + timedelta(days=days)
            days += 1
            if d == date.today():
                return

            filename = self.filename(
                name,
                '{:04d}'.format(d.year),
                '{}.{:04d}.{:02d}.{:02d}.json'.format(
                    name,
                    d.year,
                    d.month,
                    d.day
            ))
            yield d, filename

    def sync_heartrate_intraday(self):
        '''
        Downloads heartrate intraday data from the FitBit API
        to the local data store
        '''
        for d, filename in self.day_filenames('heartrate_intraday'):
            if os.path.isfile(filename):
                log.info('Cached: %s', filename)
                continue

            log.info('Downloading: %s', filename)
            hr = self.client.get_heartrate_intraday(d)
            self.write(filename, hr)

    def sync_activities(self):
        '''
        Downloads daily activities data from the FitBit API
        to the local data store
        '''
        for d, filename in self.day_filenames('activities'):
            if os.path.isfile(filename):
                log.info('Cached: %s', filename)
                continue

            log.info('Downloading: %s', filename)
            hr = self.client.get_activities(d)
            self.write(filename, hr)

    def get_sleep(self):
        '''
        Return sleep data from the local store.
        Returns: [{sleep_data}, ...]
        where `sleep_data` is the inner dict from
        https://dev.fitbit.com/build/reference/web-api/sleep/
        '''
        sleep = []
        for dir, dirs, files in os.walk(self.filename('sleep')):
            for file in files:
                filename = os.path.join(dir, file)
                data = json.load(open(filename))
                if not data:
                    continue
                sleep.extend(data)
        return sleep

    def get_heartrate_intraday(self):
        '''
        Return heartrate intraday data from the local store.
        Returns: [{hr_data}, ...]
        where `hr_data` is:
        {
            "date": "2016-07-08",
            "minutes": [int, ...]
        }
        minutes is an array of 1440 minutes in the day and the HR during that minute
        '''

        def compress(data):
            minutes = [None] * 24 * 60
            for o in data:
                h, m, s = map(int, o['time'].split(':'))
                i = h * 60 + m
                minutes[i] = o['value']
            return minutes

        heartrate = []
        for d, filename in self.day_filenames('heartrate_intraday'):
            if not os.path.isfile(filename):
                continue
            data = json.load(open(filename))
            if not data:
                continue
            heartrate.append({
                'date': d.isoformat(),
                'minutes': compress(data),
            })
        return heartrate
