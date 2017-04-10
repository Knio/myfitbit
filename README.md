# MyFitbit

Because *"Your data belongs to you!"*

...and fitbit's own data export sucks.

## Installation

Recommended:

```sh
pip3 install myfitbit
```

Manual:

```sh
git clone git@github.com:Knio/myfitbit
cd myfitbit
python3 setup.py install
```

## Usage

```sh
python3 -m myfitbit --help
```

```python
import myfitbit
import datetime

f = myfitbit.Fitbit()
f.login(username="user@fitbit.com", password="hunter2")
user_info = f.user_info()
```

`user_info`:

```json
{
  "locale": "en_US",
  "subscriptions": {
    "trainer": {
      "active": false,
      "premium": false,
      "trial": false
    }
  },
  "trackerType": "ATOM",
  "isAdmin": false,
  "bmr": 1634.1234,
  "facebookTokenExpired": false,
  "trainerPlan": false,
  "hasFacebookLinked": false,
  "apiUrl": "web-api.fitbit.com",
  "isTileDashAvailable": true,
  "timezone": "America/Los_Angeles",
  "pushToNewTiles": true,
  "encodedId": "1A2BCD",
  "isFitbitEmployee": false,
  "deviceFeatures": {
    "SLEEP": true,
    "GROK": true,
    "SED_TIME": true,
    "CALORIES": true,
    "PPG": true,
    "BEDTIME_REMINDERS": true,
    "STEPS": true,
    "INACTIVITY_ALERTS": true,
    "VO2_MAX_DEMOGRAPHIC": true,
    "EXERCISE": true,
    "GPS": true,
    "ALARMS": true,
    "HEART_RATE": true,
    "NO_DEVICE": false,
    "SMART_SLEEP": true
  },
  "isDisableOldTiles": true,
  "corporateUser": false,
  "heightSystem": "METRIC",
  "email": "user@fitbit.com",
  "isOnlySoftTrackerUser": false,
  "isEmailVerificationRequired": false,
  "startDayOfWeek": 1,
  "isUserFemale": true,
  "roles": [],
  "displayName": "User Username",
  "hasPremium": false,
  "clock12": false,
  "isEmailInviteWizardEnabled": true,
  "oauth2Token": "<snip>",
  "waterId": 109,
  "weightSystem": "METRIC",
  "enableSTTile": true,
  "dateCreated": "2017-04-08T12:34:45.000",
  "id": 123456789,
  "isBadgesTileUsingAjax": true,
  "isSoftTrackerUser": false,
  "distanceUnit": "METRIC"
}
```

```python
sleep = f.get_sleep(datetime.date(2017, 4, 8))
```

`sleep`:

```json
{
  "summary": {
    "totalMinutesAsleep": 380,
    "totalTimeInBed": 430,
    "stages": {
      "rem": 120,
      "light": 190,
      "deep": 60,
      "wake": 60
    },
    "totalSleepRecords": 1
  },
  "sleep": [
    {
      "levels": {
        "data": [
          {
            "dateTime": "2017-04-08T22:55:00.000",
            "seconds": 780,
            "level": "wake"
          },
          {
            "dateTime": "2017-04-08T23:10:00.000",
            "seconds": 120,
            "level": "light"
          },
          {
            "dateTime": "2017-04-08T23:11:00.000",
            "seconds": 900,
            "level": "rem"
          },
          ...
        ],
        "summary": {
          "rem": {
            "thirtyDayAvgMinutes": 110,
            "minutes": 120,
            "count": 10
          },
          "light": {
            "thirtyDayAvgMinutes": 200,
            "minutes": 200,
            "count": 25
          },
          "deep": {
            "thirtyDayAvgMinutes": 80,
            "minutes": 60,
            "count": 4
          },
          "wake": {
            "thirtyDayAvgMinutes": 50,
            "minutes": 60,
            "count": 20
          }
        },
        "shortData": [
          {
            "dateTime": "2017-04-08T23:55:00.000",
            "seconds": 90,
            "level": "wake"
          },
          {
            "dateTime": "2017-04-09T00:05:00.000",
            "seconds": 60,
            "level": "wake"
          },
          ...
        ]
      },
      "timeInBed": 409,
      "logId": 12345678901,
      "type": "stages",
      "startTime": "2017-04-08T23:00:00.000",
      "duration": 25000000,
      "minutesToFallAsleep": 0,
      "minutesAsleep": 380,
      "isMainSleep": true,
      "minutesAfterWakeup": 0,
      "minutesAwake": 60,
      "dateOfSleep": "2017-04-08",
      "efficiency": 95
    }
  ]
}
```


## TODO:

```python
hr = f.get_heartrate(datetime.date(2017, 4, 8))
```

`hr`:

```json
{ ... }
```

