#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Wed Jun  6 00:25:58 2018

@author: ananda
"""

import twython
import astra
import colored
import json
import os
from datetime import datetime
import tweepy
class XpalTwitterStreamer(twython.TwythonStreamer):
    def __init__(self,ofile,logger,*args, **kwargs):
        super(XpalTwitterStreamer,self).__init__(*args, **kwargs)
        self.ofile=ofile
        self.buffer=[]
        self.logger=logger
    def flush_buffer(self):
        ofilejson=[]
        if os.path.exists(self.ofile):
            with open(self.ofile,"r") as f:
                ofilejson=json.loads(f.read())
        ofilejson+=self.buffer
        with open(self.ofile,"w") as f:
            f.write(json.dumps(ofilejson))
        self.buffer=[]
    def on_success(self, data):
        #self.logger.info(data)
        self.buffer.append(data)
        if len(self.buffer)>10:
            self.flush_buffer()
    def on_error(self, status_code, data):
        print(status_code)

        # Want to stop trying to get data because of the error?
        # Uncomment the next line!
        # self.disconnect()
class XpalTwitterSheeter(XpalTwitterStreamer):
     def __init__(self,sheetname,logger,*args, **kwargs):
        super(XpalTwitterStreamer,self).__init__(*args, **kwargs)
        #self.
def get_twython_streamer(config,ofilename=None,logger=astra.baselogger):
    
    if ofilename==None:
        ts=datetime.now()
        ofilename="/tmp/TwythonStreamer-"+ts.strftime("%Y%b%d-%H%M%S"+".json")
    logger.info("Trying to get a twython streamer to work with twitter streams")
    app_key=config.get("Twython",'app_key')
    app_secret=config.get("Twython",'app_secret')
    oauth_token=config.get("Twython",'oauth_token')
    oauth_token_secret=config.get("Twython",'oauth_token_secret')
    try:
        t=XpalTwitterStreamer(ofilename,logger,app_key,app_secret,oauth_token,oauth_token_secret)
        logger.info("Streamer logging at "  + colored.stylize(t.ofile,colored.fg("yellow")))
        return t
    except Exception as e:
		logger.error("Could not get twython streamer because %s" %repr(e))
		return None
    
#Get a Twython to work with twitter
def get_twython(config,logger=astra.baselogger):
    logger.info("Trying to get a twython to work with twitter")
    app_key=config.get("Twython",'app_key')
    app_secret=config.get("Twython",'app_secret')
    oauth_token=config.get("Twython",'oauth_token')
    oauth_token_secret=config.get("Twython",'oauth_token_secret')
    try:
		t=twython.Twython(app_key,app_secret,oauth_token,oauth_token_secret)	
		return t
    except Exception as e:
		logger.error("Could not get twython config because %s" %repr(e))
		return None

def get_tweepy(twconfig,logger=astra.baselogger):
    logger.info("Trying to get a tweepy to work with twitter")
    app_key=twconfig.get("Twython",'app_key')
    app_secret=twconfig.get("Twython",'app_secret')
    oauth_token=twconfig.get("Twython",'oauth_token')
    oauth_token_secret=twconfig.get("Twython",'oauth_token_secret')
    auth=tweepy.OAuthHandler(app_key,app_secret)
    auth.set_access_token(oauth_token,oauth_token_secret)
    try:
        tweep=tweepy.API(auth)
        return tweep
    except Exception as e:
        logger.error("Could not get a tweepy because %s" %repr(e))
        