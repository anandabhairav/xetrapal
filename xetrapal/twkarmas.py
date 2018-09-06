#coding: utf-8
'''
यहां हम फेसबुक सम्बन्धी अस्त्रों का उल्लेख करेंगे 
'''
#from .astra import *
import astra
import colored
import karma
import pandas
import datetime
import math

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
    results=tw.search(q=searchstring,count=tcount,tweet_mode="extended")['statuses'] 
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

		
def twython_get_ntweets_for_search(tw,search,tcount,geocode=None,maxtries=0,logger=astra.baselogger):
    #tweets=[]
    p=pandas.DataFrame(tw.search(q=search,count=tcount,tweet_mode="extended")['statuses'])
    if len(p)>0:
        tweetdf=p.drop_duplicates(subset="full_text",keep="first").reset_index()
    else: 
        return pandas.DataFrame()
    tries=0
    if maxtries==0:
        maxtries=(tcount/20)*3
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

def get_tweet_density(tw,screen_name,logger=astra.baselogger):
    last100=tw.get_user_timeline(screen_name=screen_name,count=100)
    last100=pandas.DataFrame(last100)
    if "created_at" in last100.columns:
        #last100['createdts']=last100.created_at.apply(lambda x:datetime.datetime.strptime(x.replace("+0000","UTC"),"%a %b %d %H:%M:%S %Z %Y"))
        last100['createdts']=last100.created_at.apply(get_twitter_ts)
        #m=last100.createdts.max()-last100.createdts.min()
        if len(last100)<100:
            logger.info("Account "+screen_name+" has less than 100 tweets")
        else:
            logger.info("Account "+screen_name+" has more than 100 mentions")
        logger.info("Calculating density as number of tweets divided or 100 by hours since oldest tweet or 100th oldest tweet")
        m=get_age(last100.createdts.min())
        density=len(last100)/m
        return round(density,3)
    else:
        return 0

#To move into Xetrapal
def get_twitter_ts(string):
    return datetime.datetime.strptime(string.replace("+0000","UTC"),"%a %b %d %H:%M:%S %Z %Y")

#To move into Xetrapal
def get_age(createdts):
    now=datetime.datetime.now()
    age=now-createdts
    return math.ceil(age.total_seconds()/3600)

#To =move into Xetrapal
def get_mention_density(tw,screen_name,logger=astra.baselogger):
    last100=twython_get_ntweets_for_search(tw,"@"+screen_name,tcount=100)
    last100=pandas.DataFrame(last100)
    if "created_at" in last100.columns:
        #last100['createdts']=last100.created_at.apply(lambda x:datetime.datetime.strptime(x.replace("+0000","UTC"),"%a %b %d %H:%M:%S %Z %Y"))
        last100['createdts']=last100.created_at.apply(get_twitter_ts)
        #m=last100.createdts.max()-last100.createdts.min()
        if len(last100)<100:
            logger.info("Account "+screen_name+" has less than 100 mentions")
        else:
            logger.info("Account "+screen_name+" has more than 100 mentions")
        logger.info("Calculating density as number of mentions divided by  hours since oldest mention or 100th oldest mention")
        m=get_age(last100.createdts.min())
        density=len(last100)/m
        return round(density,3)
    else:
        return 0
    
