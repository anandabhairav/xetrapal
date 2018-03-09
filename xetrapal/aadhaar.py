
#Configparser to load and read our configs
import ConfigParser
#Time to keep time, OS to work with Linux, and Datetime to keep track of dates
import time,os,urllib2
#JSON to store everything
import json
#To get some colored outputs
from pygments import highlight, lexers, formatters
from datetime import datetime

XPAL_FIELD_STYLES={'hostname': {'color': 'magenta'}, 'programname': {'color': 'cyan'}, 'name': {'color': 'cyan', 'bold': True}, 'levelname': {'color': 'green', 'bold': True}, 'asctime': {'color': 'green'}}

XPAL_LEVEL_STYLES={'info': {'color': 'blue'}, 'notice': {'color': 'magenta'}, 'verbose': {}, 'success': {'color': 'green', 'bold': True}, 'spam': {'color': 'green', 'faint': True}, 'critical': {'color': 'red', 'bold': True}, 'error': {'color': 'red'}, 'debug': {'color': 'green'}, 'warning': {'color': 'yellow'}}

XPAL_CONSOLE_FORMAT="%(asctime)s %(name)s-[%(funcName)s] %(levelname)s : %(message)s"

XPAL_LOG_FORMAT="%(asctime)s %(hostname)s %(name)s[%(funcName)s] %(levelname)s : %(message)s"

XPAL_WAIT_TIME={"short":5,"medium":10,"long":30}


def get_color_json(dictionary):
	formatted_json=get_formatted_json(dictionary)
	colorful_json = highlight(unicode(formatted_json, 'UTF-8'), lexers.JsonLexer(), formatters.TerminalFormatter())
	return colorful_json

def get_formatted_json(dictionary):
	formatted_json=json.dumps(dictionary,sort_keys=True, indent=4)
	return formatted_json

def load_config(configfile):
	config=ConfigParser.ConfigParser()
	config.read(configfile)
	return config

def load_data_from_json(jsonpath):
	data={}
	if os.path.exists(jsonpath):
		try:
	
			with open(jsonpath) as f:
				data=json.load(f)
		except Exception as e:
			print "Failed to load file because" + str(e)
	return data
	
def save_data_to_jsonfile(data,filename=None,path=None,prefix=None,suffix=None):
		if path==None:
			path=""
		if filename==None:
			filename=str(uuid4())
		if prefix != None:
			filename=prefix+filename
		if suffix != None:
			filename=filename+suffix
		fname=os.path.join(path,filename)
		with open(fname,"w") as f:
			f.write(json.dumps(data,indent=4,sort_keys=True))
		return fname
def download_file(url,path=None,filename=None,prefix=None,suffix=None):
		if path==None:
			path="."
		if filename==None:
			filename=str(uuid4())
		if prefix != None:
			filename=prefix+filename
		if suffix != None:
			filename=filename+suffix
		try:
			response = urllib2.urlopen(url)
			data=response.read()
			fname=os.path.join(path,filename)
			f=open(fname,"w")
			f.write(data)
			f.close()
			
			return fname
		except:
			return None
