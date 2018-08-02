#coding: utf-8
'''
यहां हम फेसबुक सम्बन्धी अस्त्रों का उल्लेख करेंगे 
'''
#from .astra import *
import astra
import colored
import karma
import pandas
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

def twython_search(tw,searchstring,logger=astra.baselogger,tcount=100,maxtries=10):
    results=[]
    logger.info("Searching Twitter for " + searchstring)
    results=tw.search(q=searchstring,count=tcount)['statuses'] 
    #logger.info("Got " + str(len(results)))
    tries=0
    while len(results)<tcount:
        if tries > maxtries:
            break
        maxid=results[-1]['id']
        results=results+tw.search(q=searchstring,count=tcount,max_id=maxid)['statuses']
        karma.wait(logger=logger)
        tries+=1
    logger.info("Got " + str(len(results))+ " for search query " + searchstring)
    return results[:tcount]

		
def twython_get_ntweets_for_search(tw,search,tcount,geocode=None,maxtries=50,logger=astra.baselogger):
    #tweets=[]
    p=pandas.DataFrame(tw.search(q=search,count=tcount,tweet_mode="extended")['statuses'])
    tweetdf=p.drop_duplicates(subset="full_text",keep="first").reset_index()
    tries=0
    while len(tweetdf)<tcount:
        logger.info("Currently have %s tweets" %len(tweetdf))
        if "id" in p.columns:
            p=pandas.DataFrame(tw.search(q=search,count=tcount,tweet_mode="extended",max_id=p['id'].iloc[-1])['statuses'])
        else:
            logger.info(p.columns)
        logger.info("Got %s more tweets" %len(p))
        if len(p)>1:
            p=p.drop_duplicates(subset="full_text",keep="first").reset_index(drop=True)
        else:
            logger.info("Empty tweetset")
            break
        logger.info("%s tweets are unique" %len(p))
        tweetdf=pandas.concat([tweetdf,p])
        tweetdf=tweetdf.drop_duplicates(subset="full_text",keep="first").reset_index(drop=True)
        logger.info("Sleeping...")
        karma.wait(logger=logger)
        logger.info("Got %s tweets" %len(tweetdf))
        tries+=1
        if(tries>maxtries):
            break
    return tweetdf.head(tcount)     