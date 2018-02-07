"""
collect.py
"""

from TwitterAPI import TwitterAPI
import pickle
import sys
import time

consumer_key = 'Enter your consumer key'
consumer_secret = 'Enter your secret key'
access_token = 'Enter your access token'
access_token_secret = 'Enter your access token secret key'


def get_twitter():
    return TwitterAPI(consumer_key, consumer_secret, access_token, access_token_secret)


def robust_request(twitter, resource, params, max_tries=5):

    for i in range(max_tries):
        request = twitter.request(resource, params)
        if request.status_code == 200:
            return request
        else:
            print('Got error %s \nsleeping for 15 minutes.' % request.text)
            sys.stderr.flush()
            time.sleep(61 * 15)


def main():
    twitter = get_twitter()
    tweets = []
    n_tweets = 1500
    
    # Searching Tweets related to H1b
    req = robust_request(twitter, 'search/tweets', {'q': 'h1b', 'count': 100})
    
    for r in req:
        tweets.append(r)
        if len(tweets) >= n_tweets:
            break
    t_id = tweets[-1]['id']
    
    
    for rang in range(0, 9):
        req = robust_request(twitter, 'search/tweets', {'q': 'h1b', 'count': 100, 'max_id': t_id})
       
        for r1 in req:
            tweets.append(r1)
        t_id = tweets[-1]['id']
        
        
    for t in tweets:
        if t['user']['lang'] == 'en':
            pickle.dump(tweets, open('collected_tweets.pkl', 'wb'))
        else:
            pass
        
        
    network_file = open("network.txt", "w+")
    
    
    screenname_list=[]
    
    for t1 in tweets:
        if t1['user']['protected'] == False:
            screenname_list.append(t1['user']['screen_name'])
            
    for sn in set(screenname_list[:15]):
        request=robust_request(twitter,'followers/ids', {'screen_name': sn,'count': 50})
        
        for r2 in request:
            network_file.write("%s,%s\n" %(sn,r2))



if __name__ == '__main__':
    main()
