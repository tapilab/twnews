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
#from multiprocessing import Process, Queue
from threading import Thread
from Queue import Queue
import time

from twitter.api import TwitterHTTPError
import twutil

from . import __data__
from .balance import load_balance_scores


def do_search(twapi, qu, url, score, count=100, result_type='recent'):
    domain = url[7:]
    while True:
        try:
            # TODO: catch ValueError("No JSON object could be decoded"), thrown by Python twitter api.
            result = twapi.search.tweets(q=domain, count=100, result_type='recent')
            tweets = []
            for tweet in result['statuses']:
                tweet['url_query'] = url
                tweet['url_score'] = score
                tweets.append(tweet)
            qu.put(tweets)
            return
        except TwitterHTTPError as e:
            print 'Error: ', e.e.code
            time.sleep(300)
        except ValueError as e:
            print 'Error: ', e
            qu.put(None)
            return


def search_for_tweets(scores, fname=__data__ + '/tweets.json'):
    out = codecs.open(fname, 'a', 'utf-8')
    twapi = twutil.api.twapi
    qu = Queue()
    while True:
        for url, score in scores.iteritems():
            p = Thread(target=do_search, args=(twapi, qu, url, score))
            p.start()
            p.join(900)
            if p.is_alive():
                print 'no results after 15 minutes for', url, '. continuing.'
            else:
                results = qu.get()
                if results:
                    print 'found', len(results), 'for domain', url
                    for tweet in results:
                        out.write(json.dumps(tweet) + '\n')
                time.sleep(2)


if __name__ == '__main__':
    scores = load_balance_scores()
    search_for_tweets(scores)
