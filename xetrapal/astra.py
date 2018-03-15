#coding: utf-8
#from .karma import *
#for colored logs
import os
import coloredlogs, logging
#For google sheets
import pygsheets
#For twitter
import twython
#For youtube 
#Selenium to automate browser work
from selenium import webdriver

#from selenium.webdriver.common.action_chains import ActionChains
#BeautifulSoup to make sense of what we got
#from BeautifulSoup import BeautifulSoup

#To make copies of files
#from shutil import copyfile

#Getting our basics
from .aadhaar import  XPAL_CONSOLE_FORMAT,XPAL_LEVEL_STYLES,XPAL_FIELD_STYLES


#Getting a logger which keeps track of things on console
def get_xpal_logger(name):
	xpallogger=logging.getLogger(name)
	coloredlogs.install(level="DEBUG",logger=xpallogger,fmt=XPAL_CONSOLE_FORMAT,level_styles=XPAL_LEVEL_STYLES,field_styles=XPAL_FIELD_STYLES)
	return xpallogger

baselogger=get_xpal_logger("XetrapalRoot")

#Get a Twython to work with twitter
def get_twython(config,logger=baselogger):
	logger.info("Trying to get a twython to work with twitter")
	try:
		t=twython.Twython(app_key=config.get("Twython",'app_key'),app_secret=config.get("Twython",'app_secret'),oauth_token=config.get("Twython",'oauth_token'),oauth_token_secret=config.get("Twython",'oauth_token_secret'))	
		return t
	except Exception as e:
		logger.error("Could not get twitter config because %s" %str(e))
		return None
		
#Get a pygsheet to work with Google sheets
def get_googledriver(config,logger=baselogger):
	logger.info("Trying to log into Google drive")
	try:
		gc=pygsheets.authorize(outh_file=config['outhfile'],outh_nonlocal=True,outh_creds_store=config['outhstore'])
		return gc
	except Exception as e:
		logger.error("Could not get twitter config because %s" %str(e))
		return None

#Getting a browser that lets us do browser based tasks
def get_browser(headless=False,logger=baselogger):
	logger.info("Launching a browser....")
	if headless==True:
		logger.info("...which has no head")
		os.environ['MOZ_HEADLESS'] = '1'
	
	firefox_profile = webdriver.FirefoxProfile()
	firefox_profile.set_preference("browser.privatebrowsing.autostart", True)
	#firefox_profile.set_preference("browser.download.dir", self.sessiondownloadpath);
	firefox_profile.set_preference("browser.download.folderList", 2);
	firefox_profile.set_preference("browser.download.manager.showWhenStarting", False);
	firefox_profile.set_preference("browser.helperApps.neverAsk.saveToDisk", "text/plain, text/csv",)
	driver = webdriver.Firefox(firefox_profile=firefox_profile)
	return driver
