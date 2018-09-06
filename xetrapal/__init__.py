
#coding: utf-8
'''
__________
< Xetrapal (क्षेत्रपाल) >
 ----------
        \   ^__^
         \  (oo)\_______
            (__)\       )\/\
                ||----w |
                ||     ||

हिन्दी में सोशियल मीडिया का अध्ययन 
'''

'''
यह एक इनिट फ़ाइल है, जो कि पाइथन के हर पैकेज में होनी अनिवार्य है। 
'''

__author__ = 'Ananda Bhairav Nath <anandabhairavnath@gmail.com>'
__version__ = '0.0.1'




#Named tuples help in keeping things in order
from collections import namedtuple
#To make copies of objects
from copy import deepcopy

'''
यहां हम अपने पैकेज के सब पैकेज लोड कर रहे हैं
किसी भी सब पैकेज को समझने के लिये उसके पाइथन फ़ाइल को देखें, 
जैसे की, aadhaar नामक सब पैकेज के बारे में जानने के लिये aadhaar.py नामक फ़ाइल देखें  
'''
from .aadhaar import *  
from .astra import *
from .jeeva import *
from .vaahan import *
from .Xetrapal import *




	
