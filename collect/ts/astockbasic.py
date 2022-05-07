import sys
from library.config import config
from library.mysql import mysql
from collect.ts.helper import tsSHelper
from library.monitor import tsMonitor
from library.alert import alert
import traceback


class tsAStockBasic:
    @tsMonitor
    def stock_basic(pro,db):
        tsSHelper.getDataAndReplace(pro,'stock_basic','astock_basic',db)

      
    @tsMonitor  
    def trade_cal(pro,db):
        tsSHelper.getDataAndReplace(pro,'trade_cal','astock_trade_cal',db)

        
    @tsMonitor
    def namechange(pro,db):
        tsSHelper.getDataAndReplace(pro,'namechange','astock_namechange',db)

    
    @tsMonitor   
    def hs_const(pro,db):
        table='astock_hs_const'
        mysql.exec("drop table if exists "+table+"_tmp",db)
        engine=mysql.getDBEngine(db)
        data = pro.hs_const(hs_type='SH')
        data.to_sql('astock_hs_const_tmp', engine, index=False, if_exists='append', chunksize=5000)
        data = pro.hs_const(hs_type='SZ')
        data.to_sql('astock_hs_const_tmp', engine, index=False, if_exists='append', chunksize=5000)
        mysql.exec('rename table '+table+' to '+table+'_old;',db);
        mysql.exec('rename table '+table+'_tmp to '+table+';',db);
        mysql.exec("drop table if exists "+table+'_old',db)
       
    @tsMonitor 
    def stock_company(pro,db):
        table='astock_stock_company'
        mysql.exec("drop table if exists "+table+"_tmp",db)
        engine=mysql.getDBEngine(db)
        data = pro.stock_company(exchange='SZSE', fields='ts_code,exchange,chairman,manager,secretary,reg_capital,setup_date,province,city,introduction,website,email,office,employees,main_business,business_scope')
        data.to_sql('astock_stock_company_tmp', engine, index=False, if_exists='append', chunksize=5000)
        data = pro.stock_company(exchange='SSE', fields='ts_code,exchange,chairman,manager,secretary,reg_capital,setup_date,province,city,introduction,website,email,office,employees,main_business,business_scope')
        data.to_sql('astock_stock_company_tmp', engine, index=False, if_exists='append', chunksize=5000)
        mysql.exec('rename table '+table+' to '+table+'_old;',db);
        mysql.exec('rename table '+table+'_tmp to '+table+';',db);
        mysql.exec("drop table if exists "+table+'_old',db)
    
    @tsMonitor
    def stk_managers(pro,db):
        tsSHelper.getDataAndReplace(pro,'stk_managers','astock_stk_managers',db)



    @tsMonitor
    def stk_rewards(pro,db):
        table='astock_stk_rewards'
        mysql.exec("drop table if exists "+table+"_tmp",db)
        engine=mysql.getDBEngine(db)
        data=tsSHelper.getAllAStock(True,pro,db)
        stock_list=data['ts_code'].tolist()
        
        for i in range(0,len(stock_list),100):
            code_list=stock_list[i:i+100]
            while True:
                try:
                    df = pro.stk_rewards(ts_code=','.join(code_list))
                    df.to_sql('astock_stk_rewards_tmp', engine, index=False, if_exists='append', chunksize=5000)
                    break
                except Exception as e:
                    if "最多访问" in str(e):
                        print(self.func.__name__+":触发限流，等待重试。\n"+str(e))
                        time.sleep(15)
                        continue
                    else:
                        info = traceback.format_exc()
                        alert.send('stk_rewards','函数异常',str(info))
                        print(info)
                        break
            
        mysql.exec('rename table '+table+' to '+table+'_old;',db);
        mysql.exec('rename table '+table+'_tmp to '+table+';',db);
        mysql.exec("drop table if exists "+table+'_old',db)
        
    @tsMonitor       
    def new_share(pro,db):
        tsSHelper.getDataAndReplace(pro,'new_share','astock_new_share',db)

    