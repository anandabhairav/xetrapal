from .astra import *


def fb_login(browser,fbconfig,logger=baselogger):
		fbusr=fbconfig.get("Facebook","fbusername")
		fbpwd=fbconfig.get("Facebook","fbpassword")
		# or you can use Chrome(executable_path="/usr/bin/chromedriver")
		logger.info("Trying to log into FB in browser...")
		try:
			browser.get("http://www.facebook.com")
			assert "Facebook" in browser.title
			elem = browser.find_element_by_id("email")
			elem.send_keys(fbusr)
			elem = browser.find_element_by_id("pass")
			elem.send_keys(fbpwd)
			elem.send_keys(Keys.RETURN)
			time.sleep(10)
			self.goto_url("http://facebook.com/profile.php",browser=browser)
			time.sleep(10(
			logger.info("Successfully logged into FB")
		except Exception as exception:
			logger.error("Could not log into FB.."+ repr(exception))
	
