import json

import dominate
from dominate.tags import *
from dominate.util import *

def make_report(sleep):
    doc = dominate.document(title='Sleep Report')

    with doc.head:
        style(include('static/report.css'))
        script(src='http://dominate.js.zkpq.ca/dominate.min.js')
        script(src="https://cdnjs.cloudflare.com/ajax/libs/d3/4.12.0/d3.js", integrity="sha256-0Lzb1mm7+96oAeDnxAPpfdRdi6jLYTV9XTVt4p6kPg0=", crossorigin="anonymous")
        # script(src="https://cdnjs.cloudflare.com/ajax/libs/d3-axis/1.0.8/d3-axis.js", integrity="sha256-xVKXY9dQ9Yi0FkLKQkZFzTj2clkkJ0cb4XPk83xnCMo=", crossorigin="anonymous")
        script(
            raw('var sleep = '),
            raw(json.dumps(sleep, indent=2, sort_keys=2)),
            raw(';')
        )

    with doc.body:
        div('Sleep')
        div(id='chart')
        script(include('static/chart.js'))


    return doc.render()


def main():
    sleep = json.load(open('sleep.json'))
    html = make_report(sleep)
    with open('sleep.html', 'w') as f:
        f.write(html)

if __name__ == '__main__':
    main()
