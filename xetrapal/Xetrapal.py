import os
from .aadhaar import *
from .astra import *
from .vaahan import *


class Xetrapal(object):
	def __init__(self,configfile):
		self.jsonprofile={}
		self.config=load_config(configfile)
		self.name=self.config.get("Xetrapal","name")
		self.logger=get_xpal_logger(self.name)
		self.set_property("name",self.name)
		self.datapath=self.config.get("Xetrapal","datapath")
		self.set_property("datapath",self.datapath)
		self.jsonfile=os.path.join(self.datapath,"xetrapal.json")
		self.set_property("jsonfile",self.jsonfile)
		if os.path.exists(self.jsonfile):
			fileprofile=load_data_from_json(self.jsonfile)
			if fileprofile!={}:
				self.jsonprofile=fileprofile
		self.save_profile()
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
		self.logger.info("Saving own JSON profile to file %s" %self.jsonfile)
		save_data_to_jsonfile(self.jsonprofile,filename=self.jsonfile)
	
	
	def add_vaahan_twitter(self):
		self.twitter=get_twython(self.config,logger=self.logger)
	
	def add_vaahan_facebook(self):
		self.logger.info("Trying to get a Facebook vaahan")
