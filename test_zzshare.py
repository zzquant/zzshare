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
    token=os.getenv("ZZSHARE_TOKEN", "fake-token-for-test"), # 在环境变量中获取,或者明确写到这里
)

# 直接打印出 api 支持的所有接口名字
# print([method for method in dir(api) if not method.startswith('_')])
# 注意检查 pyproject.toml 中的 version 是否与实际版本一致
# git push
# git tag v0.4.13
# git push origin v0.4.13

# 获取日线行情
# df = api.daily(ts_code='920978.BJ', start_date='20250101', end_date='20250131')
# print(df)



# df = api.daily(ts_code='000001', start_date='20260302', end_date='20260331')
# print(df)

# df = api.daily(
#     ts_code='600871',
#     start_date='20050101',
#     end_date='20260203',
#     adj='qfq',

# )
# print(df)

df = api.daily(trade_date='20260331',limit=10)
print(df)

df = api.daily(trade_date='20260410',limit=10, fields='ts_code,trade_date,open,close,high,low,volume,amount,adjustflag,turnoverrate')
print(df)


# # df = api.daily(trade_date='20260410',limit=10000, fields='all') 
# # print(df.shape) # 5495

basic = api.stock_basic(exchange='', list_status='L', fields='ts_code,symbol,name,exchange,list_status')
print(basic)

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


# 板块列表
# plates = api.plates_list(plate_type=17)
# print(plates)
# 板块排名
# plates = api.plates_rank(plate_type=17, date1='20260417', limit=20)
# print(plates)
#板块下个股列表,按照人气排名
# stocks = api.market_plate_stocks(plate_type=17, plate_code='801660',date1='20260416', limit=3)
# print(stocks)

# 同花顺全A,主要用来查看全市场成交量
# response = api.plate_kline(b_code="883957", date1="20260101", date2="20260428")
# print(response)

#涨跌分布
# print(api.updown_distribution("20260513"))
#情绪数据
# print(api.open_sentiment_data("20260511","20260513"))
# print(api.sentiment_timing("20260601","20260601"))
#题材数据
# print(api.topic_table_list())


# 1. 查询 2024-12-31 的日频估值数据 (默认 source 为 jq)
# df_val = api.finance_valuation("2025-12-31")
# print(df_val.head())

# ---------------- 板块分时数据（1分钟级别分时走势 / 分钟K线） ----------------
# 说明区分：
# 1. api.trend_minute(code, [date], [as_df]):
#    获取个股或板块的分钟级真实分时走势（每交易日 241 个 1 分钟点位，包含时间、价格/点位、均价、成交量、涨跌幅等）。
#    支持板块代码（如概念板块 '801660'）以及个股代码。
# 2. api.plates_trend(plate_type, plate_code, day_start, day_end):
#    获取板块日级别历史指标走势（每日一行，包含当日涨跌幅、主力资金、热度排名等）。

# (1) 板块最新/当日 1 分钟级分时数据 (返回原始 Dict)
print("\n=== 1. 板块当日分时走势 (1分钟分时点位，原始数据) ===")
fenshi_dict = api.trend_minute(code='801660')
if isinstance(fenshi_dict, dict):
    print(f"板块代码: {fenshi_dict.get('code')}, 日期: {fenshi_dict.get('day')}, 昨收点位: {fenshi_dict.get('preclose_px')}")
    print(f"分时分钟数: {len(fenshi_dict.get('trend', []))} 根")
    print("前 3 根分时 [时间, 点位, 均价, 成交量, 方向]:", fenshi_dict.get('trend', [])[:3])
else:
    print(fenshi_dict)

# (2) 板块分钟级分时数据直接转为 DataFrame
print("\n=== 2. 板块当日分时走势 (DataFrame 格式) ===")
df_fenshi = api.trend_minute(code='801660', as_df=True)
print(df_fenshi.head(10))
print(df_fenshi.tail(5))

# (3) 查询指定历史日期的板块 1 分钟级分时走势
print("\n=== 3. 板块历史某日分时走势 (2026-10-30) ===")
df_fenshi_his = api.trend_minute(code='801660', date='2026-10-30', as_df=True)
print(f"历史分时记录数: {len(df_fenshi_his)} 条")
if not df_fenshi_his.empty:
    print(df_fenshi_his[['trade_time', 'price', 'avg_price', 'vol', 'pct_chg']].head())

# (4) 区别说明：板块日级别历史走势与指标数据 (每日 1 条)
# daily_trend = api.plates_trend(plate_type=17, plate_code='801660', day_start='20260401', day_end='20261016')
# print(pd.DataFrame(daily_trend).head())
