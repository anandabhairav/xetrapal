"""
Created on Wed Jun  6 00:31:18 2018

@author: ananda
"""

import astra,karma,os
import sys
import telegram

def poll(botname,botstop):
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
                        botname.updater.dispatcher.process_update(update)
                        #messageparser(botname,update,handler,logger=botname.logger)
            except Exception as e:
                botname.logger.warning("Timed out, will try again in a bit {}".format(repr(e)))
        else:
            botname.logger.info(u"Stopfile found, {} exiting bot update loop".format(botname.name))
            break

def messageparser(bot,update,handler=None,logger=astra.baselogger):
    if update.message:
        logger.info(u"This looks like a message")
        
        if update.message.reply_to_message:
            source_message=update.message.reply_to_message.text
        else:
            source_message=None
        if update.message.text:
            response=update.message.text
        else:
            response=None
        if update.message.location:
            location=update.message.location.to_json()
        else:
            location=None
        reply_id=update.message.chat_id
        logger.info(u"ID: {}\nSource Message: {}\nResponse: {}\nLocation: {}".format(reply_id,source_message,response,location))
    elif update.callback_query:
        logger.info(u"This looks like a callback query")
        source_message=update.callback_query.message.text
        response=update.callback_query.data
        location=None
        reply_id=update.callback_query.message.chat_id
        logger.info(u"ID: {}\nSource Message: {}\nResponse: {}\nLocation: {}".format(source_message,response,location))
    else:
        logger.info(u"This makes no sense, a message with no callback and no message")
    parsed_update={"source_message":source_message,"response":response,"location":location,"reply_id":reply_id}
    if handler!=None:
        handler(bot,update,parsed_update,logger)
    else:
        return parsed_update