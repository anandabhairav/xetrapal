#from .aadhaar import
import os
from .aadhaar import XPAL_LOG_FORMAT
import  karma
#from .karma import *
import  astra
#from .astra import *
from datetime import datetime
import colored
#UUIDs for everyone
from uuid import uuid4

import coloredlogs,logging

class Jeeva(object):
	def __init__(self,config=None,configfile=None):
		if configfile != None:
			self.config=karma.load_config(configfile)
		else:
			self.config=config
		self.jsonprofile={}
		try:
			self.name=self.config.get("Jeeva","name")
		except:
			self.name="Jeeva-"+str(uuid4())
		self.set_property("name",self.name)
		self.logger=astra.get_xpal_logger(self.name)
		self.logger.info("My name is "+ colored.stylize(self.name,colored.fg("red")))
		self.setup_disk()
		self.setup_memory()
		self.start_session()
		#self.karta=Karta(self)
		#self.karta.start()
		self.save_profile()
		self.kartarefs=[]
		self.configfile=configfile
	def setup_disk(self):
		self.datapath=self.config.get("Jeeva","datapath")
		self.set_property("datapath",self.datapath)
		self.jeevajsonfile=os.path.join(self.datapath,"jeeva.json")
		self.set_property("jeevajsonfile",self.jeevajsonfile)
		if not os.path.exists(self.datapath):
			self.logger.info("Creating a new datapath for myself at %s" %colored.stylize(self.datapath,colored.fg("yellow")))
			os.mkdir(self.datapath)
		else:
			self.logger.info("I already have a datapath at the location %s" %colored.stylize(self.datapath,colored.fg("yellow")))

	def setup_memory(self):
		if os.path.exists(self.jeevajsonfile):
			fileprofile=karma.load_data_from_json(self.jeevajsonfile)
			if fileprofile!={}:
				self.jsonprofile=fileprofile
		self.set_property("name",self.name)

	def set_property(self,propertyname,value):
		self.jsonprofile[propertyname]=value
	def get_property(self,propertyname):
		if propertyname in self.jsonprofile.keys():
			return self.jsonprofile[propertyname]
		else:
			return None
	def show_profile(self):
		self.logger.info("\n"+karma.get_color_json(self.jsonprofile))
	def save_profile(self):
		self.logger.info("Saving own JSON profile to file %s" %colored.stylize(self.jeevajsonfile,colored.fg("yellow")))
		karma.save_data_to_jsonfile(self.jsonprofile,filename=self.jeevajsonfile)


	def log_to_disk(self):
		logFormatter=logging.Formatter(XPAL_LOG_FORMAT)
		fileHandler = logging.FileHandler("{0}/{1}.log".format(self.sessionpath, "jeevasession"))
		fileHandler.setFormatter(logFormatter)
		fileHandler.addFilter(coloredlogs.HostNameFilter())
		self.logger.addHandler(fileHandler)
		self.sessionlogfile=os.path.join(self.sessionpath,"jeevasession.log")
		self.logger.info("Saving messages to log at " + colored.stylize(self.sessionlogfile,colored.fg("yellow")))
		if os.path.exists(os.path.join(self.datapath,"xpal.log")):
			os.remove(os.path.join(self.datapath,"xpal.log"))
		os.symlink(self.sessionlogfile, os.path.join(self.datapath,"xpal.log"))
		
	def start_session(self):
		sessionpathprefix=self.config.get("Jeeva","sessionpathprefix")
		ts=datetime.now()
		sessiondir=sessionpathprefix+"-"+ts.strftime("%Y%b%d-%H%M%S")
		self.sessionpath=os.path.join(self.datapath,sessiondir)
		self.sessiondownloadpath=os.path.join(self.sessionpath,"downloads")
		self.sessionjsonpath=os.path.join(self.sessionpath,"json")
		sessiondata={}
		sessiondata['sessionpath']=self.sessionpath
		sessiondata['sessiondownloadpath']=self.sessiondownloadpath
		sessiondata['sessionjsonpath']=self.sessionjsonpath
		if not os.path.exists(self.sessionpath):
			self.logger.info("Creating a new path for this session at %s" %colored.stylize(self.sessionpath,colored.fg("yellow")))
			os.mkdir(self.sessionpath)
		if not os.path.exists(self.sessiondownloadpath):
			self.logger.info("Creating a new download path for this session at %s" %colored.stylize(self.sessiondownloadpath,colored.fg("yellow")))
			os.mkdir(self.sessiondownloadpath)
		if not os.path.exists(self.sessionjsonpath):
			self.logger.info("Creating a new json path for this session at %s " %colored.stylize(self.sessionjsonpath,colored.fg("yellow")))
			os.mkdir(self.sessionjsonpath)
		self.log_to_disk()
		sessiondata['sessionlog']=self.sessionlogfile
		self.set_property("lastsession",sessiondata)
