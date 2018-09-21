#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Wed Jun  6 00:31:18 2018

@author: ananda
"""

import astra
import sys,os,json
import pandas
from telegram.ext import MessageHandler, Filters
from telegram.ext import Updater, CommandHandler
import karma
class XetrapalTelegramBot:
    def __init__(self,config,logger=astra.baselogger):
        self.name=config.get("TelegramBot","name")
        self.statefile=config.get("TelegramBot","statefile")
        self.logger=logger
        tokenfile=config.get("TelegramBot","tokenfile")
        with open(tokenfile,"r") as f:
            token=f.read().strip()
        self.updater=Updater(token)
        self.load_state()
        if self.state=={}:
            self.users=[]
            self.offset=0
            self.save_state()


    def save_state(self):
        self.state['offset']=self.offset
        self.state['users']=self.users
        with open(self.statefile,"w") as f:
            f.write(json.dumps(self.state))
    def load_state(self):
        if os.path.exists(self.statefile):
            with open(self.statefile,"r") as f:
                self.state=json.loads(f.read().strip())
            self.offset=int(self.state['offset'])
            self.users=self.state['users']
        else:
            self.state={}

    def get_latest_updates(self):
        self.logger.info("Trying to get latest updates for bot "+self.name)
        p=self.updater.bot.get_updates(offset=self.offset)
        if len(p)>0:
            for update in p:
                self.logger.info(u"Got message {}".format(update.to_json()))
                
                uids = [user['id'] for user in self.users]
                if update.message!=None:
                    if update.message.from_user.id not in uids:
                        self.logger.info("Adding user to user list")
                        self.users.append(json.loads(update.message.from_user.to_json()))
                    else:
                        self.logger.info("User in list already")
                else:
                    if update.callback_query:
                        self.logger.info("Callback query received")
                    else:
                        self.logger.info("Special Message")
            self.offset=p[-1].update_id+1
            self.save_state()
        else:
            self.logger.info("No new messages received for bot " + self.name)
        return p
