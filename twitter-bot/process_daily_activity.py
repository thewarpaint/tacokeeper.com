#!/usr/bin/env python
# encoding: utf-8

import locale
import os
import tweepy
from textwrap import wrap
import yaml

from time import sleep
from tweepy_helper import get_api, get_user_info
from yaml_helper import dump_user_data, load_user_data

# Testing stuff
dry_run = False

# TODO: Remove as many global variables as possible
demo_summary_file = './assets/tacokeeper-summary.png'
query = '#tacokeeper -filter:retweets'
welcome_message = '¡Hola, @{screen_name}! Tu perfil estará disponible pronto en https://tacokeeper.com/{screen_name}'
last_processed_id = '1113321710239985667'
tk_url_profile_prefix = 'https://tacokeeper.com/{screen_name}?t='
tk_url_prefix = 'https://tacokeeper.com/?t='
varieties = []

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

    data = load_user_data(tweet.user.id_str)

    if data is None:
        print('Please create the profile for user {screen_name} first'.format(screen_name = tweet.user.screen_name))
        return

    if not dry_run:
        if len(data['activities']) == 0:
            send_welcome_tweet(tweet)

        data['activities'].insert(0, tweet_info)
        data['summary']['total_tacos'] += tweet_info['total_tacos']

        new_varieties = 0

        # Add category and variety badges to entries
        for entry in tweet_info['entries']:
            if not entry['category'] in data['summary']['categories']:
                entry['badges'].append('category')
                data['summary']['categories'].append(entry['category'])
                tweet_info['badges'].append({
                    'text': 'Nueva categoría: ' + entry['category'].capitalize(),
                    'type': 'category',
                })

            if not entry['variety_key'] in data['summary']['varieties']:
                entry['badges'].append('variety')
                data['summary']['varieties'].append(entry['variety_key'])
                new_varieties += 1

        if new_varieties > 0:
            new_varieties_text = '{number} nueva variedad' if new_varieties == 1 else '{number} nuevas variedades'

            tweet_info['badges'].append({
                'text': new_varieties_text.format(number = str(new_varieties)),
                'type': 'variety',
            })

        data['summary']['total_categories'] = len(data['summary']['categories'])
        data['summary']['total_varieties'] = len(data['summary']['varieties'])

        dump_user_data(tweet.user.id_str, data)

        try:
            tweet.favorite()

            # Wait three seconds before continuing to avoid Twitter shadowbanning our favs :/
            sleep(3)
        except tweepy.TweepError:
            pass

    print('Tweet processed successfully:', tweet_info)

def send_welcome_tweet(tweet_to_reply_to):
    # Not working for some reason, perhaps spam detection?!
    # api.update_with_media(filename = demo_summary_file,
    #                       status = welcome_message.format(screen_name = tweet_to_reply_to.user.screen_name),
    #                       in_reply_to_status_id = tweet_to_reply_to.id)

    try:
        api.update_status(status = welcome_message.format(screen_name = tweet_to_reply_to.user.screen_name.lower()),
                          in_reply_to_status_id = tweet_to_reply_to.id)

        # TODO: Fix "UnicodeEncodeError: 'ascii' codec can't encode character"
        print('Sent welcome tweet successfully to {user}'.format(user = tweet_to_reply_to.user.screen_name))

        # Wait three seconds before continuing to avoid Twitter shadowbanning our welcome tweets :/
        sleep(3)

    except tweepy.TweepError as exception:
        print('Welcome tweet was probably sent already for {user}'.format(user = tweet_to_reply_to.user.screen_name))
        print(exception)

def get_tweet_info(tweet):
    tweet_info = {
        'id': tweet.id,
        'created_at': str(tweet.created_at),
        'created_at_formatted': tweet.created_at.strftime('%B %d').capitalize(),
        'tk_url': '',
        'tk_data': '',
        'badges': [],
        'type': 'daily',
    }

    if len(tweet.entities['urls']) == 1:
        tweet_info['tk_url'] = tweet.entities['urls'][0]['expanded_url']
        tweet_info['tk_data'] = get_raw_tacokeeper_data(tweet.user.screen_name, tweet_info['tk_url'])

        entries = get_activity(tweet_info['tk_data'])

        tweet_info['entries'] = entries
        tweet_info['total_tacos'] = reduce((lambda acc, entry: acc + entry['amount']), entries, 0)

    return tweet_info

def get_raw_tacokeeper_data(screen_name, url):
    profile_prefix = tk_url_profile_prefix.format(screen_name = screen_name)

    return url.replace(tk_url_prefix, '').replace(profile_prefix, '')

def get_activity(tk_data):
    if len(tk_data) % 5 != 0:
        print('TK data length must be a multiple of 5, skipping:', tk_data)
        return []

    return map(lambda x: get_entry(x), wrap(tk_data, 5))

def get_entry(variety_item):
    entry_format = u'{amount} × {variety}'
    variety_key = variety_item[0:3]
    variety_amount = int(variety_item[3:])
    variety = get_variety(variety_key)

    return {
        'amount': variety_amount,
        'badges': [],
        'category': variety['category'],
        'text': entry_format.format(amount = variety_amount, variety = variety['name']),
        'variety_key': variety['key'],
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
    locale.setlocale(locale.LC_ALL, 'es_ES')
    api = get_api()
    varieties = load_varieties()
    process_tweets(last_processed_id)

    # TODO: Add a command line option to process individual statuses
    # process_tweet(api.get_status(1102234568747335682, tweet_mode = 'extended'))
