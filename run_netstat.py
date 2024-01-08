#!/usr/bin/env python3

import argparse
from typing import List
from ipaddress import ip_address

from src.Netstat import Netstat
from src.Connection import Net_Connection

sort_keys = ('pid', 'proto', 'family', 'localAddr', 'localPort', 'remoteAddr', 'remotePort', 'state')

#TODO implement filtering by values of th keys
filter_keys = ('pid', 'proto', 'family', 'localAddr', 'localPort', 'remoteAddr', 'remotePort', 'state')

def get_connections(sort_by='pid', filter=None) -> List[Net_Connection]:
    connections = Netstat.get_connections()

    if sort_by and sort_by in sort_keys:
        #TODO: implement sorting by ip addresses:
        # if sort_by.endswith('Addr'):
        #     connections.sort(key=lambda c: ip_address(getattr(c, sort_by)))
        # else:
            connections.sort(key=lambda c: getattr(c, sort_by))

    if filter and filter in filter_keys:
        connections = [c for c in connections if getattr(c, filter) is not None]

    return connections

def print_connections(sort_by, filter):
    for connection in get_connections(sort_by, filter):
        print(connection.to_csv())

def main():
    parser = argparse.ArgumentParser(description='Display network connections.')
    parser.add_argument('--sort_by', default='pid', help='Sort connections by the specified key', choices=sort_keys)
    parser.add_argument('--filter', help='Filter connections by the specified key', choices=filter_keys)
    args = parser.parse_args()

    sort_by = args.sort_by
    filter = args.filter
    print_connections(sort_by=sort_by, filter=filter)

if __name__ == '__main__':
    main()
