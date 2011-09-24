'''
Created on 24-09-2011

Buffering Proxy - for chosen requests will accumulate partial responses 
and will call rewriteResponse() when the whole response is ready

@author: koto
'''
from twisted.web.proxy import ProxyClient
from twisted.python import log

class BufferingProxyClient(ProxyClient):
    
    # modify these in rewriteResponse
    buffer = ""
    header_buffer = {}
        
    def handleResponsePart(self, buffer):
        
        if self.needsRewrite():
            self.buffer = self.buffer + buffer
        else:
            ProxyClient.handleResponsePart(self, buffer)

    def handleResponseEnd(self):
        if self.needsRewrite():
            log.msg("Rewriting " + self.father.uri)

            # We might have increased or decreased the page size. Since we have not written
            # to the client yet, we can still modify the headers.
            self.rewriteResponse()
            self.header_buffer["content-length"] = len(self.buffer)
            for key in self.header_buffer.keys():
                ProxyClient.handleHeader(self, key, self.header_buffer[key])
            ProxyClient.handleEndHeaders(self)
            ProxyClient.handleResponsePart(self, self.buffer) 
            
            self.buffer = ""
            self.header_buffer = {}
        
        ProxyClient.handleResponseEnd(self)
      
    def rewriteResponse(self):
        pass
    
    def needsRewrite(self):
        return False
    
    def handleHeader(self, key, val):
        if self.needsRewrite():
            self.header_buffer[key.lower()] = val
        else:
            ProxyClient.handleHeader(self, key, val) 
        
    def handleEndHeaders(self):
        if not self.needsRewrite():
            ProxyClient.handleEndHeaders(self)
