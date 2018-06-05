#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Wed Jun  6 00:25:58 2018

@author: ananda
"""

import twython
import astra

class XpalTwitterStreamer(twython.TwythonStreamer):
    def __init__(self,*args, **kwargs):
        super(XpalTwitterStreamer,self).__init__(*args, **kwargs)
        self.ofile=kwargs['ofile']
    def on_success(self, data):
        if 'text' in data:
            with open(self.ofile,"a") as f:
               f.write(data['text'])

    def on_error(self, status_code, data):
        print(status_code)

        # Want to stop trying to get data because of the error?
        # Uncomment the next line!
        # self.disconnect()

def get_twython_streamer(config,ofilename,logger=astra.baselogger):
    logger.info("Trying to get a twython to work with twitter")
    app_key=config.get("Twython",'app_key')
    app_secret=config.get("Twython",'app_secret')
    oauth_token=config.get("Twython",'oauth_token')
    oauth_token_secret=config.get("Twython",'oauth_token_secret')
    try:
		t=XpalTwitterStreamer(app_key,app_secret,oauth_token,oauth_token_secret,ofile=ofilename)	
		return t
    except Exception as e:
		logger.error("Could not get twitter config because %s" %str(e))
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
		logger.error("Could not get twitter config because %s" %str(e))
		return None