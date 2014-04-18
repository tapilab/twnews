"""
Print users who were found for multiple urls.

user url1 score1 url2 score2 ...
"""
import codecs
from collections import defaultdict
import json
import sys

from . import __data__

sys.stdout = codecs.getwriter('utf8')(sys.stdout)


def print_urls_by_user(tweets_file=__data__ + '/tweets.json'):
    user2urls = defaultdict(lambda: set())
    url2score = defaultdict(lambda: 0.)
    inf = codecs.open(tweets_file, 'rt', 'utf-8')
    for line in inf:
        js = json.loads(line)
        if 'url_query' in js:  # valid line
            user2urls[js['user']['screen_name']].add(js['url_query'])
            url2score[js['url_query']] = float(js['url_score'])
    for user, urls in user2urls.iteritems():
        if len(urls) > 1:
            print user + '\t' + '\t'.join('%s\t%.3f' % (u, url2score[u]) for u in urls)


if __name__ == '__main__':
    print_urls_by_user()
