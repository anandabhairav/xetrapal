from uuid import *
import json
from collections import namedtuple
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from BeautifulSoup import BeautifulSoup
import ConfigParser
import time,os,urllib2
from datetime import datetime
from uuid import *
from pygments import highlight, lexers, formatters
import pygsheets
DEBUG=False
from shutil import copyfile
from copy import deepcopy
import coloredlogs, logging

from Queue import Queue
from threading import Thread

XPL_FIELD_STYLES={'hostname': {'color': 'magenta'}, 'programname': {'color': 'cyan'}, 'name': {'color': 'cyan', 'bold': True}, 'levelname': {'color': 'green', 'bold': True}, 'asctime': {'color': 'green'}}

XPL_LEVEL_STYLES={'info': {'color': 'blue'}, 'notice': {'color': 'magenta'}, 'verbose': {}, 'success': {'color': 'green', 'bold': True}, 'spam': {'color': 'green', 'faint': True}, 'critical': {'color': 'red', 'bold': True}, 'error': {'color': 'red'}, 'debug': {'color': 'green'}, 'warning': {'color': 'yellow'}}

XPL_CONSOLE_FORMAT="%(asctime)s %(name)s-[%(funcName)s] %(levelname)s : %(message)s"

XPL_LOG_FORMAT="%(asctime)s %(hostname)s %(name)s[%(funcName)s] %(levelname)s : %(message)s"

XPL_WAIT_TIME={"short":5,"medium":10,"long":30}

