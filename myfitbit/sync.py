'''
Syncs a FitbitDatastore with the most recent data with a FitbitClient
'''
import os
import json
import logging
from datetime import date, time, timedelta

log = logging.getLogger(__name__)


class FitbitSync(object):
    def __init__(self, datastore, client):
        self.datastore = datastore
        self.client = client

    def sync(self):
        self.sync_profile()
        self.sync_sleep()
        self.sync_heartrate()
        self.sync_weight()
        self.sync_heartrate_intraday()
        self.sync_activities()

    def sync_profile(self):
        self.datastore.write(
            self.datastore.filename('profile.json'),
            self.client.profile)

    def sync_ranged_data(self, name, client_fn):
        '''
        Downloads date-range time series data from
        the FitBit API to the local data store, one month at a time
        '''
        fn = self.datastore.filename
        month = 2015 * 12 # TODO use profile['memberSince']
        while 1:
            date_start = date(month // 12, month % 12 + 1, 1)
            month += 1
            date_end =   date(month // 12, month % 12 + 1, 1)

            if date_start > date.today():
                break

            partial = date_end > date.today()
            partial_filename = fn(name, '{}.{:04d}.{:02d}.partial.json'.format(
                name,
                date_start.year,
                date_start.month,
            ))
            filename = fn(name, '{}.{:04d}.{:02}.json'.format(
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
            self.datastore.write(filename, data)

    def sync_sleep(self):
        self.sync_ranged_data('sleep', self.client.get_sleep_range)

    def sync_heartrate(self):
        self.sync_ranged_data('heartrate', self.client.get_heartrate_range)

    def sync_weight(self):
        self.sync_ranged_data('weight', self.client.get_weight_range)

    def sync_intraday_data(self, name, client_fn):
        '''
        Downloads intraday data from the FitBit API
        to the local data store, one day at a time
        '''
        for day, filename in self.datastore.day_filenames(name):
            if os.path.isfile(filename):
                log.debug('Cached: %s', filename)
                continue

            log.info('Downloading: %s', filename)
            data = client_fn(day)
            self.datastore.write(filename, data)

    def sync_heartrate_intraday(self):
        self.sync_intraday_data(
            'heartrate_intraday', self.client.get_heartrate_intraday)

    def sync_activities(self):
        self.sync_intraday_data(
            'activities', self.client.get_activities)
