"""
This is an example application.

It should do bandmaths, like NDVI. 
"""
import simple

@simple.annotate()
def bandmaths(chunk):
    print "computing", chunk
    import time
    import random
    time.sleep(random.random()*1)    
    return chunk + 1


