#from .aadhaar import 
import os
from .aadhaar import *
from .astra import *
from datetime import datetime
import colored
#UUIDs for everyone
from uuid import *
from Queue import Queue
import threading

def kill_jeeva(jeeva,logger=baselogger):
		logger.info("Killing jeeva " + colored.stylize(jeeva.name,colored.fg("violet")))
		jeeva.karta.kill=True
		jeeva.queue.put("Die")
		del(jeeva)
	

class Karta(threading.Thread):
	def __init__(self,jeeva):
		threading.Thread.__init__(self)
		self.jeeva = jeeva
		self.kill=False
		self.jeeva.logger.info("Karta initialized....")
		
	def run(self):
		self.jeeva.logger.info("Karta waiting for commands....\n")
		while self.kill != True:
			command=self.jeeva.queue.get()
			self.jeeva.logger.info("Got command - " + command)
			if command == "Die":
				self.jeeva.logger.info("Dying")
				self.jeeva.save_profile()
				self.kill=True
		

class Jeeva(object):
	def __init__(self,config=None,configfile=None):
		if configfile != None:
			self.config=load_config(configfile)
		else:
			self.config=config
		self.jsonprofile={}
		try:
			self.name=self.config.get("Jeeva","name")
		except:
			self.name="Jeeva-"+str(uuid4())
		self.set_property("name",self.name)
		self.logger=get_xpal_logger(self.name)
		self.logger.info("My name is "+ colored.stylize(self.name,colored.fg("red")))
		self.setup_disk()
		self.setup_memory()
		self.start_session()
		self.queue=Queue()
		self.karta=Karta(self)
		self.karta.start()
		self.save_profile()
		
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
			fileprofile=load_data_from_json(self.jeevajsonfile)
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
		self.logger.info("\n"+get_color_json(self.jsonprofile))
	def save_profile(self):
		self.logger.info("Saving own JSON profile to file %s" %colored.stylize(self.jeevajsonfile,colored.fg("yellow")))
		save_data_to_jsonfile(self.jsonprofile,filename=self.jeevajsonfile)
	

	def log_to_disk(self):
		logFormatter=logging.Formatter(XPAL_LOG_FORMAT)
		fileHandler = logging.FileHandler("{0}/{1}.log".format(self.sessionpath, "jeevasession"))
		fileHandler.setFormatter(logFormatter)
		fileHandler.addFilter(coloredlogs.HostNameFilter())
		self.logger.addHandler(fileHandler)
		self.sessionlogfile=os.path.join(self.sessionpath,"jeevasession.log")
		self.logger.info("Saving messages to log at " + colored.stylize(self.sessionlogfile,colored.fg("yellow")))
		
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
	
	def save_config(self,filename):
		self.logger.warning("Saving config file in plain text in file " + colored.stylize(filename,colored.fg("yellow")))
		with open(filename,"w") as configfile:
			self.config.write(configfile)
	
