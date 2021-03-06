#!/usr/bin/env python
# encoding: utf-8

from datetime import date, datetime
import locale
import tweepy
import sys

from tweepy_helper import get_api
from yaml_helper import dump_user_data, load_user_data

tweet_content = '''
@{screen_name} ¡Gracias por registrar tus tacos con nosotros!
En {month} registraste {total_tacos} tacos de {total_categories} {category_text} y {total_varieties} {variety_text}.
Ya actualizamos la actividad del mes en tu perfil: https://tacokeeper.com/{screen_name}
'''

send_summary_tweet = True

def run():
    locale.setlocale(locale.LC_ALL, 'es_ES')
    month_to_process = ''
    user_id = ''

    try:
        month_to_process = sys.argv[1]
    except IndexError:
        print('Missing argument: month to process')
        return

    try:
        user_id = sys.argv[2]
    except IndexError:
        print('Missing argument: user id')
        return

    process_monthly_activity(month_to_process, user_id)

def process_monthly_activity(month_to_process, user_id):
    user_data = load_user_data(user_id)
    processing_data_str = 'Processing data for month {month} and user {screen_name}'
    # TODO: make sure this is a daily type entry and not a monthly one
    in_reply_to_status_id = user_data['activities'][0]['id']

    print(processing_data_str.format(month = month_to_process, screen_name = user_data['user']['screen_name']))

    monthly_activity = get_monthly_summary(month_to_process, user_data)
    print(monthly_activity)

    user_data['activities'].insert(0, monthly_activity)
    dump_user_data(user_id, user_data)

    if send_summary_tweet:
        send_monthly_summary_tweet(user_id, user_data['user']['screen_name'], monthly_activity,
            in_reply_to_status_id)

def get_monthly_summary(month_to_process, user_data):
    # Using dictionaries to keep track of most frequent categories and varieties in the future
    categories = {}
    varieties = {}
    total_tacos = 0

    for daily_activity in user_data['activities']:
        if daily_activity['type'] != 'daily':
            continue

        if not month_to_process in daily_activity['created_at']:
            continue

        total_tacos += daily_activity['total_tacos']

        for entry in daily_activity['entries']:
            if not entry['variety_key'] in varieties:
                varieties[entry['variety_key']] = 0

            varieties[entry['variety_key']] += entry['amount']

            if not entry['category'] in categories:
                categories[entry['category']] = 0

            categories[entry['category']] += entry['amount']

    return {
        'summary': {
            'month': get_readable_month(month_to_process),
            'total_categories': len(categories),
            'total_varieties': len(varieties),
            'total_tacos': total_tacos,
        },
        'type': 'monthly',
    }

def send_monthly_summary_tweet(user_id, screen_name, monthly_activity, in_reply_to_status_id):
    api = get_api()

    # TODO: Move pluralisation forms to a YML file
    category_text = 'categoría' if monthly_activity['summary']['total_categories'] == 1 else 'categorías'
    variety_text = 'variedad' if monthly_activity['summary']['total_varieties'] == 1 else 'variedades'

    status_text = tweet_content.format(
        screen_name = screen_name,
        month = monthly_activity['summary']['month'],
        total_tacos = monthly_activity['summary']['total_tacos'],
        total_categories = monthly_activity['summary']['total_categories'],
        category_text = category_text,
        total_varieties = monthly_activity['summary']['total_varieties'],
        variety_text = variety_text,
    )

    try:
        # TODO: Restore the app's write access :(
        print(status_text)
        # api.update_status(status = status_text,
        #                   in_reply_to_status_id = in_reply_to_status_id)
        print('Sent monthly activity tweet successfully to {screen_name}'.format(screen_name = screen_name))
    except tweepy.TweepError as exception:
        print('Monthly activity tweet was probably sent already for {screen_name}'.format(screen_name = screen_name))
        print(exception)

def get_readable_month(month_to_process):
    first_day_of_month = datetime.strptime(month_to_process + '-01', '%Y-%m-%d')
    return first_day_of_month.strftime('%B')

if __name__ == '__main__':
    run()
