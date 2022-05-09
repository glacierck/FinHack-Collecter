import sys
import os
sys.path.append(os.path.dirname(os.path.realpath(__file__))+"/../")
from library.config import config
from library.mysql import mysql
from collect.ts.helper import tsSHelper

cfgTS=config.getConfig('ts')
db=cfgTS['db']

tables_list=mysql.selectToList('show tables',db)
for v in tables_list:
    table=list(v.values())[0]
    tsSHelper.setIndex(table,db)

 
