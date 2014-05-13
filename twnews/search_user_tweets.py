"""
Download up to 3,200 tweets from each user in tweets.json that matches
criteria below.
"""
import codecs
from collections import Counter, defaultdict
import json

import twutil
from . import __data__


def search_users(tweets_file=__data__ + '/tweets.json', users_file=__data__ + '/users.json', min_users=10, max_tweets_per_user=2):
    url2mentions = defaultdict(lambda: Counter())
    url2score = defaultdict(lambda: 0.)
    outf = codecs.open(users_file, 'a', 'utf-8')
    inf = codecs.open(tweets_file, 'rt', 'utf-8')
    for line in inf:
        js = json.loads(line)
        if 'url_query' in js:  # valid line
            url2mentions[js['url_query']].update([js['user']['screen_name']])
            url2score[js['url_query']] = float(js['url_score'])
    for url, mentions in url2mentions.iteritems():
        if len(mentions) >= min_users:
            users = [u for u in mentions if mentions[u] <= max_tweets_per_user]
            for user in users:
                print user
                tweets = twutil.collect.tweets_for_user(user)
                if tweets and len(tweets) > 0:
                    print 'found', len(tweets)
                    js = {'url_query': url, 'url_score': url2score[url], 'screen_name': user,
                          'tweets': tweets}
                    outf.write(json.dumps(js) + '\n')


if __name__ == '__main__':
    search_users()
