'''
Created on 24-09-2011

@author: koto
'''
from twisted.internet import reactor
from twisted.web import http
from twisted.python import log
from twisted.web.proxy import ProxyClientFactory, ProxyRequest, Proxy
import IplexProxyClient
import sys

class ProxyRunner:

    def run(self, port, proxyfactory):
        log.startLogging(sys.stdout)
        reactor.listenTCP(port, proxyfactory)
        reactor.run()


class RewriteProxyClientFactory(ProxyClientFactory):
    protocol = IplexProxyClient.IplexProxyClient
    
class RewriteProxyRequest(ProxyRequest):
    protocols = {'http': RewriteProxyClientFactory}

class RewriteProxy(Proxy):
    requestFactory = RewriteProxyRequest
    
class RewriteProxyFactory(http.HTTPFactory):
    protocol = RewriteProxy

