import sys
#For google sheets
import pygsheets
DEBUG=False
#For twitter
import twython
#For youtube 
#Selenium to automate browser work
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
#BeautifulSoup to make sense of what we got
from BeautifulSoup import BeautifulSoup
#for colored logs
import coloredlogs, logging
#To make copies of files
from shutil import copyfile

#Getting our basics
from .aadhaar import  XPAL_CONSOLE_FORMAT,XPAL_LEVEL_STYLES,XPAL_FIELD_STYLES
from .aadhaar import get_color_json,get_formatted_json,load_config,load_data_from_json



#Getting a logger which keeps track of things on console
def get_xpal_logger(name):
	xpallogger=logging.getLogger(name)
	coloredlogs.install(level="DEBUG",logger=xpallogger,fmt=XPAL_CONSOLE_FORMAT,level_styles=XPAL_LEVEL_STYLES,field_styles=XPAL_FIELD_STYLES)
	return xpallogger


baselogger=get_xpal_logger("XetrapalRoot")


