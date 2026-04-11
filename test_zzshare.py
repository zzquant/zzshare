from zzshare.client import DataApi
api = DataApi("e08bb33c3242b831be4e67f2dc0f63e53cd4a491c0a327ee6fff7df81a8256a")

# 直接打印出 api 支持的所有接口名字
# print([method for method in dir(api) if not method.startswith('_')])
# git tag v0.1.6
# git push origin v0.1.6

# 获取日线行情
df = api.daily(ts_code='920978.BJ', start_date='20250101', end_date='20250131')
print(df)

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

df = api.daily(trade_date='20260331',limit=10, fields='ts_code,open,close,high,low,volume,amount,adjustflag,turnoverrate')
print(df)


# df = api.daily(trade_date='20260410',limit=10000, fields='all') 
# print(df.shape) # 5495

# basic = api.stock_basic(exchange='', list_status='L', fields='ts_code,symbol,name,exchange,list_status')
# print(basic)

#测试获取实时日K
# real_info =  api.rt_k("3*.SZ", fields="all")
# print(real_info)
print(api.rt_k("9*.BJ", fields="all").shape)
# print(api.rt_k(ts_code='3*.SZ,6*.SH,0*.SZ,9*.BJ', fields="all").shape) # 5502
print(api.rt_k("300986.SZ", fields="all"))
print(api.rt_k("920978.BJ", fields="all"))


# df = api.daily(trade_date='20260410',limit=10000, fields='all') 
# print(api.rt_k(ts_code='3*.SZ,6*.SH,0*.SZ,9*.BJ', fields="all").shape) # 5502
