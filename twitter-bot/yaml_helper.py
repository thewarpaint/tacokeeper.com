# encoding: utf-8

import yaml

user_data_path = '../_data/twitter/{user_id}.yml'

def load_user_data(user_id):
    data = None

    try:
        read_stream = file(user_data_path.format(user_id = user_id), 'r')
        data = yaml.safe_load(read_stream)
    except IOError:
        pass

    return data

def dump_user_data(user_id, data):
    write_stream = file(user_data_path.format(user_id = user_id), 'w')
    yaml.safe_dump(data, write_stream, default_flow_style = False, encoding = 'utf-8')
