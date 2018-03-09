#from .aadhaar import 
from .astra import *

#Get a Twython to work with twitter
def get_twython(config,logger=baselogger):
	logger.info("Trying to get twitter")
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

