import os
import json
import logging
from datetime import date, time, timedelta

log = logging.getLogger(__name__)

class FitbitDatastore(object):
    '''
    Local data store of Fitbit json objects.
    '''
    def __init__(self, root):
        self.root = os.path.abspath(root)

    def filename(self, *args):
        return os.path.join(self.root, *args)

    @staticmethod
    def write(filename, data):
        dirname = os.path.dirname(filename)
        os.makedirs(dirname, exist_ok=True)
        with open(filename, 'w') as f:
            f.write(json.dumps(data, indent=2, sort_keys=True))

    @staticmethod
    def read(filename):
        return json.load(open(filename))

    def day_filenames(self, name):
        # TODO use profile['memberSince']
        start = date(2017, 1, 1)
        days = 0
        while 1:
            day = start + timedelta(days=days)
            days += 1
            if day == date.today():
                return

            filename = self.filename(
                name,
                '{:04d}'.format(day.year),
                '{}.{:04d}.{:02d}.{:02d}.json'.format(
                    name,
                    day.year,
                    day.month,
                    day.day
            ))
            yield day, filename

    def get_proile(self):
        return self.read(self.filename('profile.json'))

    def get_sleep(self):
        '''
        Return sleep data from the local store.
        Yeilds: {sleep_data}, ...
        where `sleep_data` is the inner dict from
        https://dev.fitbit.com/build/reference/web-api/sleep/
        '''
        for dir, dirs, files in os.walk(self.filename('sleep')):
            for file in files:
                filename = os.path.join(dir, file)
                data = self.read(filename)
                yield from data

    def get_activities(self):
        '''
        Return activities data from the local store.
        Yeilds: (day, {activities_data})
        where `activities_data` is the inner dict from
        https://dev.fitbit.com/build/reference/web-api/activity/
        '''
        for day, filename in self.day_filenames('activities'):
            if not os.path.isfile(filename):
                continue
            data = self.read(filename)
            yield day, data

    def get_weight(self):
        '''
        Return weight logs from the local store.
        Yeilds: {weight_data}, ...
        where `weight_data` is the inner dict from
        https://dev.fitbit.com/build/reference/web-api/body/#weight
        '''
        for dir, dirs, files in os.walk(self.filename('weight')):
            for file in files:
                filename = os.path.join(dir, file)
                data = self.read(filename)
                yield from data


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

        for d, filename in self.day_filenames('heartrate_intraday'):
            if not os.path.isfile(filename):
                continue
            data = self.read(filename)
            if not data:
                continue
            yield {
                'date': d.isoformat(),
                'minutes': compress(data),
            }
