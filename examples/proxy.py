# -*- coding: utf-8 -*-

'''
simple TCP proxy using pync.

example usage:
    proxy.py 8000 host.example.com 80
'''

import argparse
import threading

import pync


def main():
    parser = argparse.ArgumentParser('proxy.py',
            formatter_class=argparse.RawTextHelpFormatter,
            description=__doc__,
    )

    parser.add_argument('proxy_port',
        help='proxy port to listen on',
        type=int,
    )
    parser.add_argument('dest',
        help='destination host to connect to',
    )
    parser.add_argument('port',
        help='destination port to connect to',
        type=int,
    )
    args = parser.parse_args()

    server = pync.Netcat(
            port=args.proxy_port,
            v=True,
            l=True,
            stdin=pync.PIPE,
            stdout=pync.PIPE,
    )
    t = threading.Thread(target=server.readwrite)
    t.daemon = True
    t.start()

    client = pync.Netcat(args.dest, args.port,
            v=True,
            stdin=server.stdout,
            stdout=server.stdin,
    )

    try:
        client.readwrite()
    finally:
        client.close()
        server.close()


if __name__ == '__main__':
    main()
