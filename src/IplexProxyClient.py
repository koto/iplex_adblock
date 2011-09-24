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
from xml.etree.ElementTree import ElementTree, XMLTreeBuilder, tostring
from twisted.python import log

class ElementTreeFromString(ElementTree):

    def parse(self, source, parser=None):
        if not parser:
            parser = XMLTreeBuilder()
        parser.feed(source)
        self._root = parser.close()
        return self._root
        
class IplexProxyClient(BufferingProxyClient.BufferingProxyClient):
    
    def needsRewrite(self):
        if re.search("iplex\.pl/player_feed/", self.father.uri):
            return True
        return False
    
    def rewriteResponse(self):
        tree = ElementTreeFromString()
        tree.parse(self.buffer)
        self.removeSequenceItems(tree)
        self.removeMediaItems(tree)
        
        self.buffer = tostring(tree.getroot(),'utf-8')

    def removeMediaItems(self, tree):
        container = tree.find('//Media')
        count = 0
        total = 0
        for el in tree.findall('//MediaItem'):
            total = total + 1 
            if re.match('A',el.get('id')):
                container.remove(el) # remove ads
                count = count + 1
            else:
                el.set('type', 'primary')
        
        log.msg("Total media items: " + str(total)+ ", removed " + str(count))        

    def removeSequenceItems(self, tree):
        container = tree.find('//Sequence')
        count = 0
        total = 0
        for el in tree.findall('//SequenceItem'):
            total = total + 1 
            if re.match('A',el.get('id')):
                container.remove(el) # remove ads
                count = count + 1
            else:
                el.set('type', 'primary')
        
        log.msg("Total sequence items: " + str(total)+ ", removed " + str(count))        
        