# encoding: utf-8

import os
import tweepy

def get_api():
    auth = tweepy.OAuthHandler(os.environ['TKB_CONSUMER_KEY'], os.environ['TKB_CONSUMER_SECRET'])
    auth.set_access_token(os.environ['TKB_ACCESS_TOKEN'], os.environ['TKB_ACCESS_TOKEN_SECRET'])

    return tweepy.API(auth)

def get_user_info(user):
    user_info = {
        'id': user.id_str,
        'profile_image_url': user.profile_image_url_https.replace('_normal', ''),
        'screen_name': user.screen_name.lower()
    }

    return user_info
