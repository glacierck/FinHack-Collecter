import sys
import datetime
from library.config import config
from library.mysql import mysql
from collect.ts.helper import tsSHelper
from library.monitor import tsMonitor
import time
import pandas as pd
import traceback
from library.alert import alert

class tsCB:
    @tsMonitor
    def cb_basic(pro,db):
        tsSHelper.getDataAndReplace(pro,'cb_basic','cb_basic',db)
        
    
    @tsMonitor
    def cb_issue(pro,db):
        tsSHelper.getDataWithLastDate(pro,'cb_issue','cb_issue',db,'ann_date')
        
    @tsMonitor
    def cb_call(pro,db):
        tsSHelper.getDataAndReplace(pro,'cb_call','cb_call',db)
        
    @tsMonitor
    def cb_daily(pro,db):
        tsSHelper.getDataWithLastDate(pro,'cb_daily','cb_daily',db)
   
   
    @tsMonitor
    def cb_price_chg(pro,db):
        tsSHelper.getDataAndReplace(pro,'cb_price_chg','cb_price_chg',db)     
        
     
        
        