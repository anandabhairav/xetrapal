#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Fri Mar 16 12:19:01 2018

@author: anandabhairav
"""


import pykka
class Karta(pykka.ThreadingActor):
    def __init__(self,jeeva):
        super(Karta,self).__init__()
        #threading.Thread.__init__(self)
        self.jeeva = jeeva
        self.jeeva.logger.info("Karta initialized....")
    def on_start(self):
        self.jeeva.logger.info("Karta started")
        
    def on_receive(self,message):
        self.jeeva.logger.info("Received message " + str(message))
        if message['msg']=="run":
            self.jeeva.logger.info("Trying to run " + str(message['func']))
            #message['kwargs']['logger']=self.jeeva.logger
            try:
                message['func'](*message['args'],**message['kwargs'])
            except Exception as e:
                self.jeeva.logger.error(repr(e))
        if message['msg']=="get":
            self.jeeva.logger.info("Trying to get a return value from " + str(message['func']))
            try:
                returnvalue=message['func'](*message['args'],**message['kwargs'])
                return returnvalue
            except Exception as e:
                return repr(e)