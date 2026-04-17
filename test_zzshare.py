import zzshare
import os
import pandas as pd
from zzshare import DataApi
# pd.set_option('display.max_columns', None)  # 显示所有列
# pd.set_option('display.width', 1000)        # 设置显示宽度

# 初始化日志
zzshare.set_level('INFO')


api = DataApi(
    # 获取地址:https://quant.zizizaizai.com/me/profile
    token=os.getenv("ZZSHARE_TOKEN1", "fake-token-for-test"), # 在环境变量中获取,或者明确写到这里
)

# 直接打印出 api 支持的所有接口名字
# print([method for method in dir(api) if not method.startswith('_')])
# git tag v0.2.0
# git push origin v0.2.0

# 获取日线行情
# df = api.daily(ts_code='920978.BJ', start_date='20250101', end_date='20250131')
# print(df)



df = api.daily(ts_code='000001', start_date='20260302', end_date='20260331')
print(df)

df = api.daily(
    ts_code='600871',
    start_date='20260101',
    end_date='20260203',
    adj='qfq'
)
print(df)

df = api.daily(trade_date='20260331',limit=10)
print(df)

df = api.daily(trade_date='20260410',limit=10, fields='ts_code,trade_date,open,close,high,low,volume,amount,adjustflag,turnoverrate')
print(df)



# # df = api.daily(trade_date='20260410',limit=10000, fields='all') 
# # print(df.shape) # 5495

# # basic = api.stock_basic(exchange='', list_status='L', fields='ts_code,symbol,name,exchange,list_status')
# # print(basic)

# #测试获取实时日K
# # real_info =  api.rt_k("3*.SZ", fields="all")
# # print(real_info)
# print(api.rt_k("9*.BJ", fields="all").shape)
# # print(api.rt_k(ts_code='3*.SZ,6*.SH,0*.SZ,9*.BJ', fields="all").shape) # 5502
# print(api.rt_k("300986.SZ", fields="all"))
# print(api.rt_k("920978.BJ", fields="all"))


# # df = api.daily(trade_date='20260410',limit=10000, fields='all') 
# # print(api.rt_k(ts_code='3*.SZ,6*.SH,0*.SZ,9*.BJ', fields="all").shape) # 5502

# stock_list = api.stock_basic(exchange='',fields='ts_code,name,exchang')
# print(stock_list.head(3))

# # 获取某日1分钟K线
# df = api.stk_mins(ts_code='600000.SH',  trade_time='20260413', freq='1min')
# print(df)