"""
Print statistics about the tweets collected by search_url_tweets.py
"""
import codecs
from collections import Counter, defaultdict
import json

import numpy as np

from . import __data__


def print_all(fname=__data__ + '/tweets.json'):
    url2mentions = defaultdict(lambda: Counter())
    url2score = defaultdict(lambda: 0.)
    inf = codecs.open(fname, 'rt', 'utf-8')
    ids = set()
    for line in inf:
        js = json.loads(line)
        if 'url_query' in js:  # valid line
            if js['id'] not in ids:
                url2mentions[js['url_query']].update([js['user']['screen_name']])
                url2score[js['url_query']] = float(js['url_score'])
                ids.add(js['id'])
    cons_mentions = dict([(url, mention) for url, mention in url2mentions.iteritems() if url2score[url] < 0])
    lib_mentions = dict([(url, mention) for url, mention in url2mentions.iteritems() if url2score[url] > 0])
    print '%25s %s' % ('# urls:', len(url2mentions))
    print '%25s %d' % ('# tweets:', sum(sum(c.itervalues()) for c in url2mentions.itervalues()))
    print '%25s %d' % ('# users:', len(set([k for c in url2mentions.itervalues() for k in c.keys()])))
    print '%25s %d' % ('# url-user pairs:', sum(len(c) for c in url2mentions.itervalues()))
    print '%25s %d' % ('# users w/1 tweet:', len(set([k for c in url2mentions.itervalues() for k in c.keys() if c[k] == 1])))
    print '%25s %d' % ('# liberal tweets:', sum(sum(c.itervalues()) for c in lib_mentions.itervalues()))
    print '%25s %d' % ('# conservative tweets:', sum(sum(c.itervalues()) for c in cons_mentions.itervalues()))
    print '%25s %.3f' % ('avg. url score:', np.mean(url2score.values()))


if __name__ == '__main__':
    print_all()
