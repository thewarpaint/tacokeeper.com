# encoding: utf-8

import os
import tweepy

def get_api():
    auth = tweepy.OAuthHandler(os.environ['TKB_CONSUMER_KEY'], os.environ['TKB_CONSUMER_SECRET'])
    auth.set_access_token(os.environ['TKB_ACCESS_TOKEN'], os.environ['TKB_ACCESS_TOKEN_SECRET'])

    return tweepy.API(auth)
