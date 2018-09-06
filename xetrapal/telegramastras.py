#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Wed Jun  6 00:31:18 2018

@author: ananda
"""

import astra
import sys

from telegram.ext import MessageHandler, Filters
from telegram.ext import Updater, CommandHandler

class XetrapalBot:
    def __init__(self,name,tokenfile,logger=astra.baselogger):
        self.name=name
        self.logger=logger
        with open(tokenfile,"r") as f:
            self.token=f.read().strip()
        self.updater=Updater(self.token)
        self.offset=0
    def get_latest_updates(self):
        self.logger.info("Trying to get latest updates for bot "+self.name)
        p=self.updater.bot.get_updates(offset=self.offset)
        if len(p)>0:
            for update in p:
                logger.info("Got message {} from user {}, id {}".format(update.message.text,update.message.from_user.first_name,update.message.from_user.id))
            self.offset=p[-1].update_id+1
        return p
    
