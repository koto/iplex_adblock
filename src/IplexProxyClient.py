'''
Created on 24-09-2011

Modifies iplex.pl player feeds to remove ads
Will probably work for other sites using vividas.com player
 
@author: koto
@see: http://blog.kotowicz.net
@license: GPL
'''
import BufferingProxyClient
import re
import IplexRewriter
from twisted.python import log
        
class IplexProxyClient(BufferingProxyClient.BufferingProxyClient):
    
    def needsRewrite(self):
        if re.search("iplex\.pl/player_feed/", self.father.uri):
            return True
        return False
    
    def rewriteResponse(self):
        rewriter = IplexRewriter.IplexRewriter(log)
        self.buffer = rewriter.rewrite(self.buffer)

