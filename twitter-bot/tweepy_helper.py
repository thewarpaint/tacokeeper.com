# encoding: utf-8

import os
import tweepy
import urllib

user_profile_image_path = 'assets/images/twitter/{screen_name}.jpg'
user_profile_relative_image_path = '../' + user_profile_image_path
user_profile_absolute_image_path = 'https://tacokeeper.com/' + user_profile_image_path

def get_api():
    auth = tweepy.OAuthHandler(os.environ['TKB_CONSUMER_KEY'], os.environ['TKB_CONSUMER_SECRET'])
    auth.set_access_token(os.environ['TKB_ACCESS_TOKEN'], os.environ['TKB_ACCESS_TOKEN_SECRET'])

    return tweepy.API(auth)

def get_user_info(user):
    user_info = {
        'id': user.id_str,
        'screen_name': user.screen_name.lower(),
    }

    return user_info

def get_user_profile_image_url(user):
    return user.profile_image_url_https.replace('_normal', '')

def download_user_profile_image(user, screen_name):
    urllib.urlretrieve(get_user_profile_image_url(user),
        user_profile_relative_image_path.format(screen_name = screen_name))
