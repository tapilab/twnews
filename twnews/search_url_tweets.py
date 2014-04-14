"""
Iteratively search for tweets containing one of the URLs on in $TWNEWS_DATA/urls.tsv.

Store the result in $TWNEWS_DATA/tweets.json.

Each tweet json is modified to include two new fields:
- url_query: the url (from balance.org) submitted as a search query
- url_score: the score for that url (from balance.org)

Queries are submitted in order, and the script loops forever. When rate limit
is hit, it sleeps for 5 minutes before continuing.

Note that this will introduce duplicates, which should be filtered downstream.
"""
import codecs
import json
import time

from twitter.api import TwitterHTTPError
import twutil

from . import __data__
from .balance import load_balance_scores


def search_for_tweets(scores, fname=__data__ + '/tweets.json'):
    out = codecs.open(fname, 'a', 'utf-8')
    twapi = twutil.api.twapi
    while True:
        for url, score in scores.iteritems():
            try:
                domain = url[7:]
                result = twapi.search.tweets(q=domain, count=100, result_type='recent')
                print 'found', len(result['statuses']), 'for', domain
                for tweet in result['statuses']:
                    tweet['url_query'] = url
                    tweet['url_score'] = score
                    out.write(json.dumps(tweet) + '\n')
                time.sleep(2)
            except TwitterHTTPError as e:
                print 'Error: ', e.e.code, '   Sleeping for 5 minutes...'
                time.sleep(300)


if __name__ == '__main__':
    scores = load_balance_scores()
    search_for_tweets(scores)
