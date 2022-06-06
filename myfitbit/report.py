import json
import logging
import pkg_resources
import sys

import dominate
from dominate.tags import *
from dominate.util import *

log = logging.getLogger('myfitbit.report')

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


def main():
    import argparse
    from . import datastore
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawTextHelpFormatter
    )
    parser.add_argument('--data-dir', required=True)
    args = parser.parse_args()
    ex = datastore.FitbitDatastore(args.data_dir)
    data = {
        'sleep': list(ex.get_sleep()),
        'heartrate': list(ex.get_heartrate_intraday()),
    }
    html = make_report(data)
    with open('report.html', 'w') as f:
        f.write(html)
    log.info('Wrote report.html', file=sys.stderr)


if __name__ == '__main__':
    logging.basicConfig(level=logging.WARN)
    main()

