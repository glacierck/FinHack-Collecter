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

class tsAStockOther:
    @tsMonitor
    def margin(pro,db):
        tsSHelper.getDataWithLastDate(pro,'margin','astock_market_margin',db)
    
    @tsMonitor
    def margin_detail(pro,db):
        tsSHelper.getDataWithLastDate(pro,'margin_detail','astock_market_margin_detail',db)
    
    @tsMonitor
    def report_rc(pro,db):
        engine=mysql.getDBEngine(db)
        if True:
            while True:
                try:
                    today = datetime.datetime.now()
                    today=today.strftime("%Y%m%d")
                    lastdate=tsSHelper.getLastDateAndDelete('astock_other_report_rc','report_date',ts_code='',db=db)
                    df =pro.report_rc(start_date=lastdate, end_date=today)
                    df.to_sql('astock_other_report_rc', engine, index=False, if_exists='append', chunksize=5000)
                    break
                except Exception as e:
                    if "每天最多访问" in str(e) or "每小时最多访问" in str(e):
                        print("report_rc:触发最多访问。\n"+str(e))
                        return
                    elif "每分钟最多访问" in str(e):
                        print("report_rc:触发限流，等待重试。\n"+str(e))
                        time.sleep(15)
                        continue
                    else:
                        info = traceback.format_exc()
                        alert.send('report_rc','函数异常',str(info))
                        print(info)  
                        return
                        
 
    @tsMonitor
    def cyq_perf(pro,db):
        engine=mysql.getDBEngine(db)
        if True:
            while True:
                try:
                    today = datetime.datetime.now()
                    today=today.strftime("%Y%m%d")
                    lastdate=tsSHelper.getLastDateAndDelete('astock_other_cyq_perf','trade_date',ts_code='',db=db)
                    df =pro.cyq_perf(start_date=lastdate, end_date=today)
                    df.to_sql('astock_other_cyq_perf', engine, index=False, if_exists='append', chunksize=5000)
                    break
                except Exception as e:
                    if "每天最多访问" in str(e) or "每小时最多访问" in str(e):
                        print("cyq_perf:触发最多访问。\n"+str(e))
                        return
                    elif "每分钟最多访问" in str(e):
                        print("cyq_perf:触发限流，等待重试。\n"+str(e))
                        time.sleep(15)
                        continue
                    else:
                        info = traceback.format_exc()
                        alert.send('cyq_perf','函数异常',str(info))
                        print(info)   
                        return
 

    @tsMonitor
    def cyq_chips(pro,db):
        engine=mysql.getDBEngine(db)
        if True:
            while True:
                try:
                    today = datetime.datetime.now()
                    today=today.strftime("%Y%m%d")
                    lastdate=tsSHelper.getLastDateAndDelete('astock_other_cyq_chips','trade_date',ts_code='',db=db)
                    df =pro.cyq_chips(start_date=lastdate, end_date=today)
                    df.to_sql('astock_other_cyq_chips', engine, index=False, if_exists='append', chunksize=5000)
                    break
                except Exception as e:
                    if "每天最多访问" in str(e) or "每小时最多访问" in str(e):
                        print("cyq_chips:触发最多访问。\n"+str(e))
                        return
                    elif "每分钟最多访问" in str(e):
                        print("cyq_chips:触发限流，等待重试。\n"+str(e))
                        time.sleep(15)
                        continue
                    else:
                        info = traceback.format_exc()
                        alert.send('cyq_chips','函数异常',str(info))
                        print(info)     
                        return
    
    
    
    
    #broker_recommend