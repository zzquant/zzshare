from zzshare.client import DataApi
api = DataApi()

# 直接打印出 api 支持的所有接口名字
# print([method for method in dir(api) if not method.startswith('_')])
# 获取日线行情
df = api.daily(ts_code='920978.BJ', start_date='20250101', end_date='20250131')
print(df)

basic = api.stock_basic(exchange='', list_status='L', fields='ts_code,symbol,name,exchange,list_status')
print(basic)
