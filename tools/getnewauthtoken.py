#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Fri Mar 16 18:12:28 2018

@author: anandabhairav
"""

t=twython.Twython(appkey,appsecret)
tcred=t.get_authentication_tokens()
authclient=twython.Twython(appkey,appsecret,tcred['oauth_token'],
tcred['oauth_token_secret'])
tcred['auth_url']
realcreds=authclient.get_authorized_tokens(<PINHERE>)
twconf.set("Twython","oauth_token",realcreds['oauth_token'])
twconf.set("Twython","oauth_token_secret",realcreds['oauth_token_secret'])
with open("<FILENAME>","w") as f:
    twconf.write(f)
secondc=twython.Twython(appkey,appsecret,realcreds['oauth_token'],realcreds['oauth_token_secret'])
secondc.update_status(status="Xetrapal काम पर है!  https://github.com/anandabhairav/xetrapal")
