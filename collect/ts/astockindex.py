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
from collect.ts.helper import tsSHelper

class tsAStockIndex:

    @tsMonitor
    def index_basic(pro,db):
        tsSHelper.getDataAndReplace(pro,'index_basic','astock_index_basic',db)
    
    @tsMonitor
    def index_daily(pro,db):
        data=tsSHelper.getAllAStockIndex(pro,db)
        index_list=data['ts_code'].tolist()
        for ts_code in index_list:
            lastdate=tsSHelper.getLastDateAndDelete('astock_index_daily','trade_date',ts_code=ts_code,db=db)
            engine=mysql.getDBEngine(db)   
            today = datetime.datetime.now()
            today=today.strftime("%Y%m%d")
            #print(ts_code)
            while True:
                try:
                    df=pro.index_daily(ts_code=ts_code, start_date=lastdate, end_date=today)
                    if(not df.empty):
                        res = df.to_sql('astock_index_daily', engine, index=False, if_exists='append', chunksize=5000)
                        #print(df)
                    break
                except Exception as e:
                    if "每天最多访问" in str(e) or "每小时最多访问" in str(e):
                        print("index_daily':触发最多访问。\n"+str(e)) 
                        return
                    if "最多访问" in str(e):
                        print('index_daily'+":触发限流，等待重试。\n"+str(e))
                        time.sleep(15)
                        continue
                    else:
                        info = traceback.format_exc()
                        alert.send('index_daily','函数异常',str(info))
                        
                        print('index_daily'+"\n"+info)
                        break                
                

    @tsMonitor
    def index_weekly(pro,db):
        tsSHelper.getDataWithLastDate(pro,'index_weekly','astock_index_weekly',db)
    
    @tsMonitor
    def index_monthly(pro,db):
        tsSHelper.getDataWithLastDate(pro,'index_monthly','astock_index_monthly',db)
    
    # @tsMonitor
    # def index_weight(pro,db):
    #     tsSHelper.getDataWithLastDate(pro,'index_weight','astock_index_weight',db)
    
    @tsMonitor
    def index_dailybasic(pro,db):
        tsSHelper.getDataWithLastDate(pro,'index_dailybasic','astock_index_dailybasic',db)
    
    @tsMonitor
    def index_classify(pro,db):
        tsSHelper.getDataAndReplace(pro,'index_classify','astock_index_classify',db)
    
    # @tsMonitor
    # def index_member(pro,db):
    #     tsSHelper.getDataWithCodeAndClear(pro,'index_member','astock_index_member',db)
    #     pass
    
    @tsMonitor
    def daily_info(pro,db):
        tsSHelper.getDataWithLastDate(pro,'daily_info','astock_index_daily_info',db)
    
    @tsMonitor
    def sz_daily_info(pro,db):
        tsSHelper.getDataWithLastDate(pro,'sz_daily_info','astock_index_sz_daily_info',db)
    
    # @tsMonitor
    # def index_weekly(pro,db):
    #     data=tsSHelper.getAllAStockIndex(pro,db)
    #     index_list=data['ts_code'].tolist()
    #     for ts_code in index_list:
    #         lastdate=tsSHelper.getLastDateAndDelete('astock_index_weekly','trade_date',ts_code=ts_code,db=db)
    #         engine=mysql.getDBEngine(db)   
    #         today = datetime.datetime.now()
    #         today=today.strftime("%Y%m%d")
    #         #print(ts_code)
    #         while True:
    #             try:
    #                 df=pro.index_weekly(ts_code=ts_code, start_date=lastdate, end_date=today)
    #                 if(not df.empty):
    #                     res = df.to_sql('astock_index_weekly', engine, index=False, if_exists='append', chunksize=5000)
    #                     #print(df)
    #                 break
    #             except Exception as e:
    #                 if "最多访问" in str(e):
    #                     print('index_daily'+":触发限流，等待重试。\n"+str(e))
    #                     time.sleep(15)
    #                     continue
    #                 else:
    #                     info = traceback.format_exc()
    #                     alert.send('index_weekly','函数异常',str(info))
                        
    #                     print('index_weekly'+"\n"+info)
    #                     break      
                    
    
    # @tsMonitor
    # def index_monthly(pro,db):
    #     data=tsSHelper.getAllAStockIndex(pro,db)
    #     index_list=data['ts_code'].tolist()
    #     for ts_code in index_list:
    #         lastdate=tsSHelper.getLastDateAndDelete('astock_index_monthly','trade_date',ts_code=ts_code,db=db)
    #         engine=mysql.getDBEngine(db)   
    #         today = datetime.datetime.now()
    #         today=today.strftime("%Y%m%d")
    #         #print(ts_code)
    #         while True:
    #             try:
    #                 df=pro.index_monthly(ts_code=ts_code, start_date=lastdate, end_date=today)
    #                 if(not df.empty):
    #                     res = df.to_sql('astock_index_monthly', engine, index=False, if_exists='append', chunksize=5000)
    #                     #print(df)
    #                 break
    #             except Exception as e:
    #                 if "最多访问" in str(e):
    #                     print('index_daily'+":触发限流，等待重试。\n"+str(e))
    #                     time.sleep(15)
    #                     continue
    #                 else:
    #                     info = traceback.format_exc()
    #                     alert.send('index_monthly','函数异常',str(info))
                        
    #                     print('index_monthly'+"\n"+info)
    #                     break      
    
    @tsMonitor
    def index_weight(pro,db):
        engine=mysql.getDBEngine(db)
        #mysql.truncateTable('astock_index_weight',db)
        data=tsSHelper.getAllAStockIndex(pro,db)
        index_list=data['ts_code'].tolist()
        for ts_code in index_list:
            while True:
                try:
                    today = datetime.datetime.now()
                    today=today.strftime("%Y%m%d")
                    lastdate=tsSHelper.getLastDateAndDelete('astock_index_weight','trade_date',ts_code=ts_code,db=db)
                    df = pro.index_weight(index_code=ts_code,start_date=lastdate, end_date=today)
                    df = df.rename({'index_code':'ts_code'}, axis='columns')
                    df.to_sql('astock_index_weight', engine, index=False, if_exists='append', chunksize=5000)
                    break
                except Exception as e:
                    if "每天最多访问" in str(e) or "每小时最多访问" in str(e):
                        print("index_weight:触发最多访问。\n"+str(e)) 
                        return
                    if "最多访问" in str(e):
                        print("index_weight:触发限流，等待重试。\n"+str(e))
                        time.sleep(15)
                        continue
                    else:
                        info = traceback.format_exc()
                        alert.send('index_weight','函数异常',str(info))
                        print(info)    
        
 
    
    # @tsMonitor
    # def index_dailybasic(pro,db):
    #     engine=mysql.getDBEngine(db)
    #     #mysql.truncateTable('astock_index_weight',db)
    #     data=tsSHelper.getAllAStockIndex(pro,db)
    #     index_list=['000001.SH','000300.SH ','000905.SH','399001.SZ','399005.SZ','399006.SZ','399016.SZ ','399300.SZ']
    #     for ts_code in index_list:
    #         while True:
    #             try:
    #                 today = datetime.datetime.now()
    #                 today=today.strftime("%Y%m%d")
    #                 lastdate=tsSHelper.getLastDateAndDelete('astock_index_dailybasic','trade_date',ts_code=ts_code,db=db)
    #                 df = pro.index_dailybasic(ts_code=ts_code,start_date=lastdate, end_date=today)
    #                 df.to_sql('astock_index_dailybasic', engine, index=False, if_exists='append', chunksize=5000)
    #                 break
    #             except Exception as e:
    #                 if "最多访问" in str(e):
    #                     print("index_dailybasic:触发限流，等待重试。\n"+str(e))
    #                     time.sleep(15)
    #                     continue
    #                 else:
    #                     info = traceback.format_exc()
    #                     alert.send('index_dailybasic','函数异常',str(info))
    #                     print(info)  
    
    # @tsMonitor
    # def index_classify(pro,db):
    #     mysql.truncateTable('astock_index_classify',db)
    #     engine=mysql.getDBEngine(db)
    #     #获取申万一级行业列表
    #     df = pro.index_classify(level='L1', src='SW2021')
    #     df.to_sql('astock_index_classify', engine, index=False, if_exists='append', chunksize=5000)
    #     #获取申万二级行业列表
    #     df = pro.index_classify(level='L2', src='SW2021')
    #     df.to_sql('astock_index_classify', engine, index=False, if_exists='append', chunksize=5000)
    #     #获取申万三级级行业列表
    #     df = pro.index_classify(level='L3', src='SW2021')
    #     df.to_sql('astock_index_classify', engine, index=False, if_exists='append', chunksize=5000)


    
    @tsMonitor
    def index_member(pro,db):
        table='astock_index_member'
        mysql.exec("drop table if exists "+table+"_tmp",db)
        engine=mysql.getDBEngine(db)
        sql='select * from astock_index_classify'
        data=mysql.selectToDf(sql,db)

        index_code_list=data['index_code'].to_list()
        for index_code in index_code_list:
            while True:
                try:
                    df = pro.index_member(index_code=index_code,fileds="index_code,index_name,con_code,con_name,in_date,out_date,is_new")
                    df = df.rename({'is_new':'isnew'}, axis='columns')
                    if(not df.empty):
                        df.to_sql('astock_index_member_tmp', engine, index=False, if_exists='append', chunksize=5000)
                    break
                except Exception as e:
                    if "每天最多访问" in str(e) or "每小时最多访问" in str(e):
                        print(self.func.__name__+":触发最多访问。\n"+str(e)) 
                        return
                    if "最多访问" in str(e):
                        print("astock_index_member:触发限流，等待重试。\n"+str(e))
                        time.sleep(15)
                        continue
                    else:
                        info = traceback.format_exc()
                        alert.send('astock_index_member','函数异常',str(info))
                        print(info)  

        mysql.exec('rename table '+table+' to '+table+'_old;',db)
        mysql.exec('rename table '+table+'_tmp to '+table+';',db)
        mysql.exec("drop table if exists "+table+'_old',db)
        tsSHelper.setIndex(table,db)
    
    # @tsMonitor
    # def daily_info(pro,db):
    #     engine=mysql.getDBEngine(db)
    #     if True:
    #         while True:
    #             try:
    #                 today = datetime.datetime.now()
    #                 today=today.strftime("%Y%m%d")
    #                 lastdate=tsSHelper.getLastDateAndDelete('astock_index_daily_info','trade_date',ts_code='',db=db)
    #                 df =pro.daily_info(start_date=lastdate, end_date=today)
    #                 df.to_sql('astock_index_daily_info', engine, index=False, if_exists='append', chunksize=5000)
    #                 break
    #             except Exception as e:
    #                 if "最多访问" in str(e):
    #                     print("index_daily_info:触发限流，等待重试。\n"+str(e))
    #                     time.sleep(15)
    #                     continue
    #                 else:
    #                     info = traceback.format_exc()
    #                     alert.send('index_daily_info','函数异常',str(info))
    #                     print(info)  
    
    # @tsMonitor
    # def sz_daily_info(pro,db):
    #     engine=mysql.getDBEngine(db)
    #     if True:
    #         while True:
    #             try:
    #                 today = datetime.datetime.now()
    #                 today=today.strftime("%Y%m%d")
    #                 lastdate=tsSHelper.getLastDateAndDelete('astock_index_sz_daily_info','trade_date',ts_code='',db=db)
    #                 df =pro.sz_daily_info(start_date=lastdate, end_date=today)
    #                 df.to_sql('astock_index_sz_daily_info', engine, index=False, if_exists='append', chunksize=5000)
    #                 break
    #             except Exception as e:
    #                 if "最多访问" in str(e):
    #                     print("index_sz_daily_info:触发限流，等待重试。\n"+str(e))
    #                     time.sleep(15)
    #                     continue
    #                 else:
    #                     info = traceback.format_exc()
    #                     alert.send('index_sz_daily_info','函数异常',str(info))
    #                     print(info)  
    
    # @tsMonitor
    # def ths_daily(pro,db):
    #     pass
    #     #tsSHelper.getDataWithLastDate(pro,'ths_daily','astock_index_ths_daily',db)
    