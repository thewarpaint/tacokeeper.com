#!/usr/bin/env python
# encoding: utf-8

from datetime import date
import locale
import sys
import urllib

from tweepy_helper import get_api, get_user_info, get_user_profile_image_url
from yaml_helper import dump_user_data

user_profile_image_path = 'assets/images/twitter/{screen_name}.jpg'
user_profile_relative_image_path = '../' + user_profile_image_path
user_profile_absolute_image_path = 'https://tacokeeper.com/' + user_profile_image_path

user_profile_path = '../user_profiles/{screen_name}.html'
user_profile_template = """---
permalink: /{screen_name}
isDemo: true
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
    user = api.get_user(screen_name = screen_name)
    user_info = get_user_info(user)

    download_user_profile_image(user, user_info['screen_name'])
    create_user_data_file(user_info)
    create_user_profile_page(user_info)

def create_user_data_file(user_info):
    today = date.today()

    user_data = {
        'activities': [],
        'user': user_info,
        'summary': {
            'categories': [],
            'joined_formatted': today.strftime('%B %Y').capitalize(),
            'total_categories': 0,
            'total_tacos': 0,
            'total_varieties': 0,
            'varieties': [],
        },
    }

    user_data['user']['cover_image'] = 'making-salsa'
    user_data['user']['profile_image_url'] = user_profile_absolute_image_path.format(screen_name = user_info['screen_name'])

    dump_user_data(user_data['user']['id'], user_data)

def create_user_profile_page(user):
    user_profile_md = user_profile_template.format(id = user['id'], screen_name = user['screen_name'])

    with open(user_profile_path.format(screen_name = user['screen_name']), 'w') as file:
        file.write(user_profile_md)

def download_user_profile_image(user, screen_name):
    urllib.urlretrieve(get_user_profile_image_url(user),
        user_profile_relative_image_path.format(screen_name = screen_name))


if __name__ == '__main__':
    run()
