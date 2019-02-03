# MyFitbit

Because *"Your data belongs to you!"*

...and fitbit's own data export sucks.

[![Build Status](https://travis-ci.org/Knio/myfitbit.png?branch=master)](https://travis-ci.org/Knio/myfitbit)
[![Coverage Status](https://coveralls.io/repos/Knio/myfitbit/badge.png?branch=master)](https://coveralls.io/r/Knio/myfitbit?branch=master)
[![Code Health](https://landscape.io/github/Knio/myfitbit/master/landscape.svg?style=flat)](https://landscape.io/github/Knio/myfitbit/master)


## Installation


The recommended way to install `myfitbit` is with
[`pip`](http://pypi.python.org/pypi/pip/):

    sudo pip install myfitbit

[![PyPI version](https://badge.fury.io/py/myfitbit.svg)](http://badge.fury.io/py/myfitbit)



Manual installation:

```sh
git clone git@github.com:Knio/myfitbit
cd myfitbit
python3 setup.py install
```


## Setup

1. Register a new app at https://dev.fitbit.com/apps/new

The app should look like this:

The Callback URL must be exactly `http://localhost:8189/auth_code`

<img src="docs/fitbit_app.png" width="271" height="606">


2. Configure the API keys

Make a file `myfitbit.ini` in your working directory with the client ID and secret you got from registering the fitbit app:

```
[fitbit_auth]
client_id = 123ABCD
client_secret = 0123456789abcdef0a1b2c3d4f5
access_token_file = .myfitbit_access_token
```


2. Export your data

```
python3 -m myfitbit
```

This will open a web browser and prompt you to allow the app to access your data.

It will then begin exporting to your current working directory.

Note that the fitbit API is rate limited to 150 calls/hour, and you can query only 1 day of heartrate data at a time. If you many days of data, you will be rate limited and see an HTTP 429 error. Simply re-run the command an hour later and it will resume downloading where it left off.

3. Generate report


```
python3 -m myfitbit.report --user 123ABC
```

Use the user id seen in the output from step 2

This will generate `report.html` in your current working directory.

![Fitbit Report](docs/fitbit.png)
