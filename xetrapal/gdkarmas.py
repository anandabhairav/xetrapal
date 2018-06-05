#coding: utf-8
'''
यहां हम फेसबुक सम्बन्धी अस्त्रों का उल्लेख करेंगे 
'''
#from .astra import *
import astra
import urllib2,json
#Fire and Forget Astras, to be run with {'msg':'run','func':function_object,'args':(),'kwargs':{}}

#Get value Astras, to be run with {'msg':'get','func':function_object,'args':(),'kwargs':{}}
#Use 

		
def lookup_ssheet(gc,sheetdict,logger=astra.baselogger):
	logger.info("Looking up sheetdict")
	for ssheet in gc.list_ssheets():
		if sheetdict['id']==ssheet['id']:
			logger.info("Found by ID")
			return ssheet
		if sheetdict['name']==ssheet['name']:
			logger.info("Found by name")
			return ssheet
	return sheetdict
	
def get_ssheet(gc,key=None,name=None,logger=astra.baselogger):
	if key==None and name==None:
		return None
	if key!=None:
		return get_ssheet_by_key(gc,key)
	if name!=None:
		return get_ssheet_by_name(name)

def create_new_ssheet(gc,title,folderid=None,logger=astra.baselogger):
	for ssheet in gc.list_ssheets():
		if ssheet['name']==title:
			logger.info("Sheet exists...try a different name")
			return None
	gc.create(title,parent_id=folderid)
	for ssheet in gc.list_ssheets():
		if ssheet['name']==title:
			logger.info("Sheet %s created" %title)
			return gc.open_by_key(ssheet['id'])
	
def get_ssheet_by_name(gc,title,logger=astra.baselogger):
	for ssheet in gc.list_ssheets():
		if ssheet['name']==title:
			logger.info("Sheet " + title  + " exists...fetching")
			return gc.open_by_key(ssheet['id'])
	logger.error("Sheet does not exist...is your name correct")
	return None
def get_ssheet_by_key(gc,key,logger=astra.baselogger):
	try:
		logger.info("Trying to fetch heet " + key )
		return gc.open_by_key(key)
	except:
		return None
def get_sheet_last_row(ssheet,sheetname):
	sheet=ssheet.worksheet_by_title(sheetname)
	rownum=2
	rowval=sheet.get_row(rownum)
	if rowval==['']:
		return None
	else:
		while rowval != ['']:
			rownum+=1
			rowval=sheet.get_row(rownum)
		return sheet.get_row(rownum-1)
		
def get_json_feed(feedurl):
	response=urllib2.urlopen(feedurl)
	data=json.load(response)
	return data
	
def goto_sheet_by_key(browser,sheetkey):
	browser.get("https://docs.google.com/spreadsheets/d/"+sheetkey)

def goto_sheet_tab(browser,sheetname):
	for sheettab in browser.find_elements_by_class_name("docs-sheet-tab-name"):
		print sheettab.get_property("innerHTML")
		if sheettab.get_property("innerHTML")==sheetname:
			sheettab.click()


def build_cube(gc,sheetname=None,key=None,logger=astra.baselogger):
	if sheetname==None and key==None:
		logger.error("No remote identifier specified,local copy only")
		return None
	if sheetname != None:
		logger.info("Trying to build cube from "+sheetname)
		cubesheet=get_ssheet_by_name(sheetname)
		cubesheet=get_ssheet_by_key(key)
	return cubesheet
	
