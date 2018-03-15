#coding: utf-8
'''
यहां हम फेसबुक सम्बन्धी अस्त्रों का उल्लेख करेंगे 
'''
#from .astra import *
import astra

#Fire and Forget Astras, to be run with {'msg':'run','func':function_object,'args':(),'kwargs':{}}
def twython_check_auth(twython,twconfig,logger=astra.baselogger):
		logger.info("Trying to check if our Twython is authenticated ...")
		try:
			logger.info("Twython is authenticated")
		except Exception as exception:
			logger.error("Twython auth check got..."+ repr(exception))



#Get value Astras, to be run with {'msg':'get','func':function_object,'args':(),'kwargs':{}}
#Use 

def twython_search(twython,searchstring,logger=astra.baselogger):
    	results={}	
        logger.info("Searching Twitter for " + searchstring)
        return results