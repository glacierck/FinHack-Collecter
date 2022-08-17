# FinHack-Collecter
## A股行情、财务数据一键采集(基于tushare.pro)
![公众号FinHack炼金术](https://user-images.githubusercontent.com/6196607/167310317-73abbb70-f94a-43d7-8bcd-c598f4a5b43b.jpg)

### 使用依赖
1. Python 3.7+ 版本(我是在Python3.8下搞的)
2. https://waditu.com 至少2000积分的权限(约200元人民币)
3. 一些Python基础
4. library目录依赖FinHack-Library项目

### 使用方法
[《从零开始卷量化(51)-跟我一键拉取全部A股、基金、可转债以及期货的行情数据！》](https://mp.weixin.qq.com/s/jWH2s3gigl4M1qg27NQMaA)
1. git clone https://github.com/FinHackCN/FinHack-Collecter.git
2. git clone https://github.com/FinHackCN/FinHack-Library.git
3. rm FinHack-Collecter/library
4. ln -s \`pwd\`/FinHack-Library FinHack-Collecter/library
5. pip(3) install -r requirements.txt
6. 重命名config目录下 *.conf.example 为 *.conf
7. 根据.conf文件中的提示信息修改配置文件
8. python(3) command/cmd_collect.py 
9. 理论上不能一次跑通，请自己修bug
10. 首次运行会比较慢，请耐心等待
11. 如果数据库中创建了相关表，请自行建立索引以加快程序速度(必加字段：ts_code,trade_date,end_date)
12. 或运行 python command/cmd_setindex.py 添加索引

<img width="824" alt="image" src="https://user-images.githubusercontent.com/6196607/167270427-f41d0768-b484-4444-9352-a91e541cb5e2.png">

<img width="1134" alt="image" src="https://user-images.githubusercontent.com/6196607/167270291-5e0856a7-8e6e-4fb6-bcf6-4687836f1764.png">

### 目录结构
#### collect
* ts/collect.py 获取tushare数据的入口
* ts/helper.py 一些函数
* astockbasic.py 获取A股基础信息数据
* astockprice.py 获取A股行情数据
* astockfinance.py 获取A股财务数据
#### command
* cmd_collect.py 命令行入口
#### config
* db.conf 用来配置数据库信息
* alert.conf 用来配置异常报警信息，支持飞书和钉钉
* ts.conf 用来配置tushare.pro的token
#### library
* alert.py 封装了飞书和钉钉报警的功能
* config.py 配置读取
* monitor.py 函数报错监控注解，用于发送报警通知
* mysql.py 数据库相关操作
* thread.py 用以辅助多线程采集

### 当前支持数据(与tushare.pro一致)
#### 沪深股票
##### 基础数据
* 股票列表
* 交易日历
* 股票曾用名
* 沪深股通成分股
* 上市公司基本信息
* 上市公司管理层
* 管理层薪酬和持股
* IPO新股上市

##### 行情数据
* 日线行情
* 周线行情
* 月线行情
* 复权行情
* 复权因子
* 每日停复牌信息
* 每日指标
* 个股资金流向
* 每日涨跌停价格
* 每日涨跌停统计
* 沪深港通资金流向
* 沪深股通十大成交股
* 港股通十大成交股
* 沪深股通持股明细
* 港股通每日成交统计

##### 财务数据
* 利润表
* 资产负债表
* 现金流量表
* 业绩预告
* 业绩快报
* 分红送股数据
* 财务指标数据
* 财务审计意见
* 主营业务构成
* 财报披露日期表
 
#### 沪深参考数据
* 融资融券交易汇总
* 融资融券交易明细
* 前十大股东
* 前十大流通股东
* 龙虎榜每日明细
* 龙虎榜机构交易明细
* 股权质押统计数据
* 股权质押明细数据
* 股票回购
* 概念股分类表
* 概念股明细列表
* 限售股解禁
* 大宗交易
* 股东人数
* 股东增减持

#### 指数数据
* 指数基本信息
* 指数日线行情
* 指数周线行情
* 指数月线行情
* 指数成分和权重
* 大盘指数每日指标
* 申万行业分类
* 申万行业成分
* 沪深市场每日交易统计
* 深圳市场每日交易情况

#### 公募基金
* 基金列表
* 基金管理人
* 基金经理
* 基金规模
* 基金净值
* 基金分红
* 基金持仓
* 基金行情
* 复权因子

### 其它数据
* 期货
* 债券
* 外汇
* 港股
* 美股
* 宏观经济






