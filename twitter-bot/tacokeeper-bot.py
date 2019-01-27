#!/usr/bin/env python
# encoding: utf-8

import os
import tweepy
import yaml

# Testing stuff
dry_run = False

# TODO: Remove as many global variables as possible
demo_summary_file = './assets/tacokeeper-summary.png'
query = '#tacokeeper'
welcome_message = '¡Hola, @{screen_name}! Tu perfil estará disponible pronto en https://tacokeeper.com/u/{screen_name}'
last_processed_id = '548595190118629377'
user_data_path = './data/{user_id}.yml'

def get_api():
    auth = tweepy.OAuthHandler(os.environ['TKB_CONSUMER_KEY'], os.environ['TKB_CONSUMER_SECRET'])
    auth.set_access_token(os.environ['TKB_ACCESS_TOKEN'], os.environ['TKB_ACCESS_TOKEN_SECRET'])
    return tweepy.API(auth)

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

def dump_data(user_id, data):
    write_stream = file(user_data_path.format(user_id = user_id), 'w')
    yaml.safe_dump(data, write_stream, default_flow_style = False, encoding = 'utf-8')

def process_tweets(since_id):
    for tweet in tweepy.Cursor(api.search,
                                q = query,
                                since_id = since_id,
                                result_type = 'recent',
                                tweet_mode = 'extended').items():
        process_tweet(tweet)

def process_tweet(tweet):
    tweet_info = {
        'id': tweet.id,
        'created_at': str(tweet.created_at),
        'user_screen_name': tweet.user.screen_name,
        'user_id': tweet.user.id,
        'text': tweet.full_text
    }

    if dry_run:
        print('Tweet retrieved successfully:', tweet_info)
        return

    if len(tweet.entities['urls']) == 1:
        tweet_info['tk_url'] = tweet.entities['urls'][0]['expanded_url']
    else:
        print('Tweet without TK link, skipping:', tweet_info)
        return

    data = load_data(tweet_info['user_id'])

    if len(data['activities']) == 0:
        send_welcome_tweet(tweet)

    data['activities'].append(tweet_info)

    dump_data(tweet_info['user_id'], data)

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

if __name__ == '__main__':
    api = get_api()
    process_tweets(last_processed_id)
