# -*- coding: utf-8 -*-
"""
Created on Wed Apr 14 15:23:42 2021

@author: ilros
"""

import json
import requests
import time
import numpy as np
import datetime as dt



class TimeShift():
    
    def __init__(self, data):
        self.intervals=data
        
        
    
    

    def run(self) -> str:
        actuations=""
        a=time.struct_time(time.localtime())
        h=a.tm_hour
        m=a.tm_min
        s=a.tm_sec
        
        hlow=int(self.intervals[0][0:2])
        hhigh=int(self.intervals[1][0:2])-1
        mlow=int(self.intervals[0][3:5])
        mhigh=int(self.intervals[1][3:5])+59
        slow=int(self.intervals[0][6:8])
        shigh=int(self.intervals[1][6:8])+59
    
        if dt.datetime.now().time() >= dt.time(hlow, mlow, slow) and dt.datetime.now().time() <= dt.time(hhigh, mhigh, shigh):
            actuations='on'
        else:
            actuations='off'
          

        return actuations

        
        
    