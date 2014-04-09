"""
Fetch the list of urls scored with political bias from balancestudy.org.

Write the output to $TWNEWS_DATA/urls.tsv
"""
import codecs
import json
import requests
import sys
from . import __data__


JSON_URL = 'http://balancestudy.org/api/memevals.json'
sys.stdout = codecs.getwriter('utf8')(sys.stdout)


def fetch_balance_scores(outf=__data__ + '/urls.tsv'):
    out = codecs.open(outf, "w", "utf-8")
    js = json.loads(requests.get(JSON_URL).text)
    for url in js:
        out.write('%s\t%f\n' % (url, js[url]))
    out.close()


if __name__ == '__main__':
    fetch_balance_scores()
