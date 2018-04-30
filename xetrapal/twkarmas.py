#coding: utf-8
'''
यहां हम फेसबुक सम्बन्धी अस्त्रों का उल्लेख करेंगे 
'''
#from .astra import *
import astra
import colored
import karma
#Fire and Forget Astras, to be run with {'msg':'run','func':function_object,'args':(),'kwargs':{}}
def twython_check_auth(tw,logger=astra.baselogger):
    logger.info("Trying to check if our Twython is authenticated ...")
    try:
        creds=tw.verify_credentials()
        logger.info("Twython is authenticated as " + colored.stylize(creds['name'],colored.fg("red")))
    except Exception as exception:
        logger.error("Twython auth check got..."+ repr(exception))



#Get value Astras, to be run with {'msg':'get','func':function_object,'args':(),'kwargs':{}}
#Use 

def twython_search(tw,searchstring,logger=astra.baselogger,tcount=100):
    results=[]
    logger.info("Searching Twitter for " + searchstring)
    results=tw.search(q=searchstring,count=tcount)['statuses'] 
    #logger.info("Got " + str(len(results)))
    while len(results)<tcount:
        maxid=results[len(results)-1]['id']
        results=results+tw.search(q=searchstring,count=tcount,max_id=maxid)['statuses']
        karma.wait(logger=logger)
    logger.info("Got " + str(len(results))+ " for search query " + searchstring)
    return results[:tcount]