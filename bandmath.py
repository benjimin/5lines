"""
This is an example application.

It should do bandmaths, like NDVI. 
"""

app = __import__('5lines') # TODO: pick a valid name

@app.annotate()
def bandmaths(chunk):
    print "computing", chunk
    #import time
    #import random
    #time.sleep(random.random()*5)    
    return chunk+1


