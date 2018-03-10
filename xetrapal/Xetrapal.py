

from .Jeeva import *
class Xetrapal(Jeeva):
	def __init__(self,*args, **kwargs):
		super(Xetrapal,self).__init__(*args, **kwargs)
		self.vaahans={}
		self.astras={}
	def update_vaahans(self):
		self.logger.info("Trying to update vaahans")
		if self.vaahans=={}:
			self.logger.warning("I don't seem to have any vaahans")
		
	def update_astras(self):
		self.logger.info("Trying to update astras")
		if self.astras=={}:
			self.logger.warning("I dont seem to have any astras")
		
	
	
