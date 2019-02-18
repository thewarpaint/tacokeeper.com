#!/usr/bin/env python
# encoding: utf-8

import sys

def run():
    month_to_process = ''

    try:
        month_to_process = sys.argv[1]
    except IndexError:
        print('Missing argument: month to process')
        return

    print(month_to_process)

if __name__ == '__main__':
    run()
