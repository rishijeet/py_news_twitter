__author__ = 'Rishijeet Mishra'

import tweepy
from NewsParser.NewsParser import NewsParser
import time

def get_api(cfg):
    auth = tweepy.OAuthHandler(cfg['consumer_key'], cfg['consumer_secret'])
    auth.set_access_token(cfg['access_token'], cfg['access_token_secret'])
    return tweepy.API(auth)

def main():

    cfg = {
        "consumer_key": '',
        "consumer_secret": '',
        "access_token": '',
        "access_token_secret": ''}

    api = get_api(cfg)

    np = NewsParser(140, 5)

    for id, tweet in enumerate(np.getShortDataforTweet()[::-1], 1):
        try:
          _status = api.update_status(status=tweet)
          # Yes, tweet is called 'status' rather confusing
          print "Tweet # = {} . Success!".format(id)
        except Exception as e:
            print str(e)
            continue


if __name__ == "__main__":
    main()
