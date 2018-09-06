#coding: utf-8
#from .aadhaar import 
import jeeva
import colored


class Vaahan(jeeva.Jeeva):
	def __init__(self,*args, **kwargs):
		super(Vaahan,self).__init__(*args, **kwargs)
		self.astras={}
				
	def update_astras(self):
		self.logger.info("Trying to update astras")
		astras={}
		if self.astras=={}:
			self.logger.warning("I dont seem to have any astras")
		else:
			for astraname in self.astras.keys():
				astras[astraname]=str(type(self.astras[astraname]))
	
		self.set_property("astras",astras)
		self.save_profile()
	

	def add_astra(self,astraname,astrahandle):
		self.astras[astraname]=astrahandle
		self.update_astras()
		
	def drop_astra(self,astraname):
		self.logger.info("Dropping astra " + colored.stylize(astraname,colored.fg("violet")))
		astrahandle=self.astras.pop(astraname)
		self.update_astras()
		return astrahandle

