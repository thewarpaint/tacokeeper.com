#!/usr/bin/env python
# encoding: utf-8

from datetime import date
import locale
import sys

from tweepy_helper import get_api, get_user_info
from yaml_helper import dump_user_data

user_profile_path = '../user_profiles/{screen_name}.html'
user_profile_template = """---
permalink: /u/{screen_name}
isDemo: false
userFile: twitter-{id}
---
{{% include user-profile.html %}}
"""

def run():
    screen_name = ''

    try:
        screen_name = sys.argv[1]
    except IndexError:
        print("Missing argument: screen name")
        return

    locale.setlocale(locale.LC_ALL, 'es_ES')
    api = get_api()
    user_info = get_user_info(api.get_user(screen_name = screen_name))

    create_user_data_file(user_info)
    create_user_profile_page(user_info)

def create_user_data_file(user_info):
    today = date.today()

    user_data = {
        'activities': [],
        'user': user_info,
        'summary': {
            'categories': [],
            'joined': today.strftime('%B %Y').capitalize(),
            'total_categories': 0,
            'total_tacos': 0,
            'total_varieties': 0,
            'varieties': [],
        },
    }

    user_data['user']['cover_image'] = 'making-salsa'

    dump_user_data(user_data['user']['id'], user_data)

def create_user_profile_page(user):
    user_profile_md = user_profile_template.format(id = user['id'], screen_name = user['screen_name'])

    with open(user_profile_path.format(screen_name = user['screen_name']), 'w') as file:
        file.write(user_profile_md)


if __name__ == '__main__':
    run()
