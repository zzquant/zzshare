from zzshare.client import DataApi
api = DataApi()

# 直接打印出 api 支持的所有接口名字
# print([method for method in dir(api) if not method.startswith('_')])
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

basic = api.stock_basic(exchange='', list_status='L', fields='ts_code,symbol,name,exchange,list_status')
print(basic)


