"""
Created on Wed Jun  6 00:31:18 2018

@author: ananda
"""

import astra,karma,os
import sys
import telegram

def update_30s(botname,botstop,handler):
    while True:
        if not os.path.exists(botstop):
            botname.logger.info(u"{} waiting for messages. Touch {} to stop".format(botname.name,botstop))
            #botname.updater.start_polling()
            #botname.updater.stop()
            karma.wait(waittime="medium",logger=botname.logger)
            try:
                p=botname.get_latest_updates()
                botname.logger.info(u"{} got {} messages".format(botname.name,len(p)))
                if len(p)>0:
                    for update in p:
                        handler(botname,update,logger=botname.logger)
            except Exception as e:
                botname.logger.warning("Timed out, will try again in a bit {}".format(repr(e)))
        else:
            botname.logger.info(u"Stopfile found, {} exiting bot update loop".format(botname.name))
            break
