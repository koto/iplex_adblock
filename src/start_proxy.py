#!/usr/bin/env python
'''
Created on 24-09-2011

Start proxy server acting like AdBlock for iplex.pl - no adverts before and after the movies
You need to point your browser/connection HTTP proxy to 127.0.0.1:8080

Usage:
./start_proxy.py [port]

Default port is 8080

@author: koto
@see: http://blog.kotowicz.net
@license: GPL
'''

from helpers import ProxyRunner, RewriteProxyFactory
import sys

if __name__ == '__main__':
    if len(sys.argv) > 1:
        port = int(sys.argv[1])
    else:
        port = 8080
        
    ProxyRunner().run(port, RewriteProxyFactory())