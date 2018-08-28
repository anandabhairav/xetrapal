 #coding: utf-8

import astra
import karma
import jeeva
import fbkarmas
import twkarmas
import colored
import twastras
import gdastras
import pykkakarta
import os
#import thespiankarta	

class Xetrapal(jeeva.Jeeva):
    def __init__(self,*args, **kwargs):
        super(Xetrapal,self).__init__(*args, **kwargs)
        self.vaahans={}
        self.astras={}
        self.update_astras()
        self.update_vaahans()
        self.save_profile()
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
    
    def update_vaahans(self):
        self.logger.info("Trying to update vaahans")
        vaahans={}
        if self.vaahans=={}:
            self.logger.warning("I dont seem to have any vaahans")
        else:
            for vaahanname in self.vaahans.keys():
                vaahans[vaahanname]=str(type(self.vaahans[vaahanname]))
    
        self.set_property("vaahans",vaahans)
        self.save_profile()
    

    def add_vaahan(self,vaahan):
        self.vaahans[vaahan.name]=vaahan
        self.update_vaahans()
    
    def release_vaahan(self,vaahanname):
        self.logger.info("Releasing vaahan " + colored.stylize(vaahanname,colored.fg("violet")))
        vaahan=self.vaahans.pop(vaahanname)
        self.update_vaahans()
        return vaahan
        

    def add_astra(self,astraname,newastra):
        self.astras[astraname]=newastra
        self.update_astras()
        
    def drop_astra(self,astraname):
        self.logger.info("Dropping astra " + colored.stylize(astraname,colored.fg("violet")))
        droppedastra=self.astras.pop(astraname)
        self.update_astras()
        return droppedastra
    def start_pykka_karta(self):
        kartaref=pykkakarta.Karta.start(jeeva=self)
        self.kartarefs.append(kartaref)
        return kartaref
   # def start_thespian_karta(self):
   #     kartaref=thespiankarta.vidhata.createActor(thespiankarta.Karta)
   #     self.kararefs.append(kartaref)
   #     return kartaref
    def get_fb_browser(self,fbconfig=None):
        if fbconfig==None:
            if "Facebook" in self.config.sections():
                fbconfig=karma.get_section(self.config,"Facebook",logger=self.logger)
                fbbrowser=astra.get_browser(logger=self.logger)
        fbkarmas.fb_login(fbbrowser,fbconfig,logger=self.logger)
        if "fbbrowser" not in self.astras.keys():
            self.add_astra('fbbrowser',fbbrowser)
        return fbbrowser
    def get_twython(self,twconfig=None):
        if twconfig==None:
            if "Twython" in self.config.sections():
                twconfig=karma.get_section(self.config,"Twython")
        tw=twastras.get_twython(twconfig,logger=self.logger)
        twkarmas.twython_check_auth(tw,logger=self.logger)
        tw.verify_credentials()
        if "twython" not in self.astras.keys():
            self.add_astra('twython',tw)
        return tw
    def get_tweepy(self,twconfig=None):
        if twconfig==None:
            if "Twython" in self.config.sections():
                twconfig=karma.get_section(self.config,"Twython")
        tweep=twastras.get_tweepy(twconfig,logger=self.logger)
        if "tweepy" not in self.astras.keys():
            self.add_astra("tweepy",tweep)
        return tweep
    def get_twython_streamer(self,twconfig=None,ofilename=None):
        if twconfig==None:
            if "Twython" in self.config.sections():
                twconfig=karma.get_section(self.config,"Twython")
        if ofilename==None:
           ofilename=os.path.join(self.sessionpath,"TwythonStreamer.json")
        tw=twastras.get_twython_streamer(twconfig,ofilename,logger=self.logger)
        if "twythonstreamer" not in self.astras.keys():
            self.add_astra('twythonstreamer',tw)
        return tw
    def get_googledriver(self,gdconfig=None):
        if gdconfig==None:
            if "Pygsheets" in self.config.sections():
                gdconfig=karma.get_section(self.config,"Pygsheets")
        gd=gdastras.get_googledriver(gdconfig,logger=self.logger)
        if "pygsheet" not in self.astras.keys():
            self.add_astra('pygsheet',gd)
        return gd
    def post_tweet(self,tweet):
        tweetmsg=karma.get_aadesh('run',self.astras['twython'].update_status,kwargs={'status':tweet})
        if self.kartarefs==[]:
            tweetkarta=self.start_pykka_karta()
        else:
            tweetkarta=self.kartarefs[0]
        tweetkarta.tell(tweetmsg)
#To Do
    def save_tweet_search_to_gdrive(self,searchstring,tcount=100,sheet_name=None):
        gd=self.astras['pygsheet']
        tw=self.astras['twython']
        