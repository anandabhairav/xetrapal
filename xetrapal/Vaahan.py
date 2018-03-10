#from .aadhaar import 
from .astra import *
from .Jeeva import *
class Vaahan(Jeeva):
	def __init__(self,*args, **kwargs):
		super(Vaahan,self).__init__(*args, **kwargs)
		self.astras={}
	def update_astras(self):
		self.logger.info("Trying to update astras")
		if self.astras=={}:
			self.logger.warning("I dont seem to have any astras")
		



	
