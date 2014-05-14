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
import sys
import traceback

import twutil

from . import __data__
from .balance import load_balance_scores


def do_search(qu, url, score, count=100, result_type='recent'):
    domain = url[7:]
    while True:
        try:
            result = twutil.collect.twapi.request('search/tweets', {'q': domain, 'count': count, 'result_type': 'recent'})
            if result.status_code == 200:
                tweets = []
                for tweet in result:
                    tweet['url_query'] = url
                    tweet['url_score'] = score
                    tweets.append(tweet)
                qu.put(tweets)
                return
            elif result.status_code in [88, 130, 420, 429]:
                print 'Sleeping off error: ', result.text
                time.sleep(300)
            else:
                sys.stderr.write('Error for %s: %s' % (domain, result.text))
                qu.put(None)
                return
        except:
            e = sys.exc_info()
            sys.stderr.write('skipping error %s\n%s' % (str(e[0]), traceback.format_exc()))
            return


def search_for_tweets(scores, fname=__data__ + '/tweets.json'):
    out = codecs.open(fname, 'a', 'utf-8')
    qu = Queue()
    while True:
        for url, score in scores.iteritems():
            p = Thread(target=do_search, args=(qu, url, score))
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
