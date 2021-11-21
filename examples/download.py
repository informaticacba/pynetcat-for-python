# -*- coding: utf-8 -*-
'''
Download client or server data to a file using pync.
'''

import argparse
import os

import pync


def main():
    parser = argparse.ArgumentParser('download.py',
            description=__doc__,
    )
    parser.add_argument('host',
            help='Hostname or ip to connect or bind to',
            nargs='?',
            default='',
            metavar='HOST',
    )
    parser.add_argument('port',
            help='Port to connect or bind to',
            metavar='PORT',
    )
    parser.add_argument('filename',
            help='Filename to save the data to',
            metavar='FILENAME',
    )
    parser.add_argument('--listen', '-l',
            help='Listen mode, for inbound connects',
            action='store_true',
    )
    args = parser.parse_args()

    mode = pync.connect
    if args.listen:
        mode = pync.listen

    with mode(args.host, args.port) as conn:
        if not os.path.exists('downloads'):
            os.makedirs('downloads')

        filepath = os.path.join('downloads', args.filename)
        with open(filepath, 'wb') as f:
            conn.readwrite(stdout=f)


if __name__ == '__main__':
    main()

