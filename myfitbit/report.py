import json
import pkg_resources
import sys

import dominate
from dominate.tags import *
from dominate.util import *

def read_resource(name):
    return pkg_resources.resource_string('myfitbit', name).decode('utf-8')

def make_report(data):
    doc = dominate.document(title='Fitbit Report')

    with doc.head:
        style(raw(read_resource('static/report.css')))
        script(src='http://dominate.js.zkpq.ca/dominate.min.js')
        script(src="https://cdnjs.cloudflare.com/ajax/libs/d3/4.12.0/d3.js", integrity="sha256-0Lzb1mm7+96oAeDnxAPpfdRdi6jLYTV9XTVt4p6kPg0=", crossorigin="anonymous")
        script(
            raw('\nvar data = '),
            raw(json.dumps(data)),
            raw(';\n')
        )

    with doc.body:
        div('Sleep')
        div(id='sleep')

        div('Heart Rate')
        div(id='heartrate')

        script(raw(read_resource('static/chart.js')))

    return doc.render()


def main(user_id):
    from . import datastore
    ex = datadtore.FitbitDatastore('.', user_id=user_id)
    data = {
        'sleep': ex.get_sleep(),
        'heartrate': ex.get_heartrate_intraday(),
    }
    html = make_report(data)
    with open('report.html', 'w') as f:
        f.write(html)
    print('Wrote report.html', file=sys.stderr)

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--user', required=True)
    args = parser.parse_args()
    main(args.user)
