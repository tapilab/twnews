"""
Print users who were found for multiple urls.

user average_score_difference url1 score1 url2 score2 ...
"""
import codecs
from collections import defaultdict
import json
import sys

from . import __data__

sys.stdout = codecs.getwriter('utf8')(sys.stdout)


def average_distance(scores):
    total = 0.
    count = 0.
    for i, si in enumerate(scores):
        for sj in scores[i + 1:]:
            total += abs(si - sj)
            count += 1.
    return total / count


def print_urls_by_user(tweets_file=__data__ + '/tweets.json'):
    user2urls = defaultdict(lambda: set())
    url2score = defaultdict(lambda: 0.)
    inf = codecs.open(tweets_file, 'rt', 'utf-8')
    ids = set()
    for line in inf:
        js = json.loads(line)
        if 'url_query' in js:  # valid line
            if js['id'] not in ids:
                user2urls[js['user']['screen_name']].add(js['url_query'])
                url2score[js['url_query']] = float(js['url_score'])
                ids.add(js['id'])
    for user, urls in user2urls.iteritems():
        if len(urls) > 1:
            dist = average_distance([url2score[u] for u in urls])
            print '%s\t%.4f\t%s' % (user, dist, '\t'.join('%s\t%.3f' % (u, url2score[u]) for u in urls))
    print 'ALL\t', average_distance(url2score.values())


if __name__ == '__main__':
    print_urls_by_user()
