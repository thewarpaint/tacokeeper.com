#!/usr/bin/env python
# encoding: utf-8

import os
import tweepy
from textwrap import wrap
import yaml

from tweepy_helper import get_api, get_user_info
from yaml_helper import dump_user_data, user_data_path

# Testing stuff
dry_run = True

# TODO: Remove as many global variables as possible
demo_summary_file = './assets/tacokeeper-summary.png'
query = '#tacokeeper -filter:retweets'
welcome_message = '¡Hola, @{screen_name}! Tu perfil estará disponible pronto en https://tacokeeper.com/u/{screen_name}'
last_processed_id = '1093600157445296129'
tk_url_prefix = 'https://tacokeeper.com/?t='
varieties = []

def load_data(user_id):
    data = None

    try:
        read_stream = file(user_data_path.format(user_id = user_id), 'r')
        data = yaml.safe_load(read_stream)
    except IOError:
        pass

    if data is None:
        data = {
            'activities': []
        }

    return data

def process_tweets(since_id):
    for tweet in tweepy.Cursor(api.search,
                                q = query,
                                since_id = since_id,
                                result_type = 'recent',
                                tweet_mode = 'extended').items():
        process_tweet(tweet)

def process_tweet(tweet):
    tweet_info = get_tweet_info(tweet)

    if tweet_info['tk_data'] == '':
        print('Tweet without TK data, skipping:', tweet_info)
        return

    data = load_data(tweet.user.id_str)

    if not dry_run:
        if len(data['activities']) == 0:
            send_welcome_tweet(tweet)
            data['user'] = get_user_info(tweet.user)

        data['activities'].insert(0, tweet_info)

        dump_user_data(tweet.user.id_str, data)

        try:
            tweet.favorite()
        except tweepy.TweepError:
            pass

    print('Tweet processed successfully:', tweet_info)

def send_welcome_tweet(tweet_to_reply_to):
    # Not working for some reason, perhaps spam detection?!
    # api.update_with_media(filename = demo_summary_file,
    #                       status = welcome_message.format(screen_name = tweet_to_reply_to.user.screen_name),
    #                       in_reply_to_status_id = tweet_to_reply_to.id)

    api.update_status(status = welcome_message.format(screen_name = tweet_to_reply_to.user.screen_name),
                      in_reply_to_status_id = tweet_to_reply_to.id)

    print('Sent welcome tweet successfully', tweet_to_reply_to.user.name, tweet_to_reply_to.id)

def get_tweet_info(tweet):
    tweet_info = {
        'id': tweet.id,
        'created_at': str(tweet.created_at),
        'text': tweet.full_text,
        'tk_url': '',
        'tk_data': ''
    }

    if len(tweet.entities['urls']) == 1:
        tweet_info['tk_url'] = tweet.entities['urls'][0]['expanded_url']
        tweet_info['tk_data'] = tweet_info['tk_url'].replace(tk_url_prefix, '')
        tweet_info['entries'] = get_activity(tweet_info['tk_data'])

    return tweet_info

def get_activity(tk_data):
    if len(tk_data) % 5 != 0:
        print('TK data length must be a multiple of 5, skipping:', tk_data)
        return

    return map(lambda x: get_entry(x), wrap(tk_data, 5))

def get_entry(variety_item):
    entry_format = '{amount} × {variety}'
    variety_key = variety_item[0:3]
    variety_amount = int(variety_item[3:])
    variety = get_variety(variety_key)

    return {
        'text': entry_format.format(amount = variety_amount, variety = variety['name'])
    }

def load_varieties():
    options = []

    try:
        read_stream = file('../_data/tacokeeper.yml', 'r')
        tacokeeper_data = yaml.safe_load(read_stream)
        options = tacokeeper_data['options']
    except IOError:
        pass

    return options

def get_variety(key):
    # TODO: Refactor this terribly expensive loop!
    return next((variety for variety in varieties if variety['key'] == key), None)


if __name__ == '__main__':
    api = get_api()
    varieties = load_varieties()
    process_tweets(last_processed_id)