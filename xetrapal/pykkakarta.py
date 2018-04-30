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
            self.jeeva.logger.info("Setting logger to own logger")
            #message['kwargs']['logger']=self.jeeva.logger
            message['func'](*message['args'],**message['kwargs'])
        if message['msg']=="get":
            self.jeeva.logger.info("Trying to run " + str(message['func']))
            self.jeeva.logger.info("Setting logger to own logger")
            try:
                returnvalue=message['func'](*message['args'],**message['kwargs'])
                return returnvalue
            except Exception as e:
                return repr(e)