import os, sys

if os.curdir not in sys.path:
    sys.path.insert(0, os.curdir)
    
     
import re
import IplexRewriter

def response(context, flow):
    if needsRewrite(flow):
        rewriter = IplexRewriter.IplexRewriter()
        flow.response.content = rewriter.rewrite(flow.response.content)

def needsRewrite(flow):
    if re.search("iplex\.pl/player_feed/", flow.request.get_url()):
        return True
    return False