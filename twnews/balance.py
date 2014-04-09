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
    """ Fetch json data and store as tab-separated file. """
    out = codecs.open(outf, "w", "utf-8")
    js = json.loads(requests.get(JSON_URL).text)
    for url in js:
        out.write('%s\t%f\n' % (url, js[url]))
    out.close()


def load_balance_scores(fname=__data__ + '/urls.tsv'):
    """ Read from tab-separated file to Python dict. """
    inf = codecs.open(fname, "r", "utf-8")
    return dict([(line.split()[0], float(line.split()[1])) for line in inf.readlines()])


if __name__ == '__main__':
    fetch_balance_scores()
    print load_balance_scores()
