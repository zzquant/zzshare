
import requests
import pandas as pd
import numpy as np

class DataApi:
    def __init__(self, token='', timeout=10, http_url='http://127.0.0.1:9001'):
        self.token = token
        self.timeout = timeout
        self.http_url = http_url

    def query(self, api_name, params=None):
        if params is None:
            params = {}
        
        url = f"{self.http_url}/{api_name}"
        try:
            res = requests.get(url, params=params, timeout=self.timeout)
            if res.status_code == 200:
                data = res.json()
                if data.get('code') == 20000:
                    return data.get('data')
                else:
                    print(f"API Error: {data.get('msg')}")
                    return None
            else:
                print(f"HTTP Error: {res.status_code}")
                return None
        except Exception as e:
            print(f"Request Error: {e}")
            return None

    def stock_basic(self, exchange='', list_status='L', fields=''):
        """
        获取基础信息
        TODO: Currently returns a limited list or dummy due to missing full stock list API.
        """
        cols = ['symbol_code', 'symbol', 'name', 'area', 'industry', 'market', 'list_date']
        return pd.DataFrame(columns=cols)

    def daily(self, symbol_code='', start_date='', end_date='', trade_date=''):
        """
        日线行情
        """
        if trade_date:
            start_date = trade_date
            end_date = trade_date

        code = symbol_code.split('.')[0]
        api_url = f"open/kline/d/{code}"
        params = {}
        if start_date:
            params['date1'] = start_date
        if end_date:
            params['date2'] = end_date
            
        data = self.query(api_url, params)
        if not data:
            return pd.DataFrame()

        dates = data.get('x', [])
        y_data = data.get('y', [])
        vols = data.get('vol', [])
        amounts = data.get('business_balance', [])

        records = []
        for i, date_str in enumerate(dates):
            if i >= len(y_data): break
            y = y_data[i]
            if len(y) < 5: continue
            
            open_px = y[0]
            close_px = y[1]
            high_px = y[2]
            low_px = y[3]
            pre_close = y[4]
            vol = vols[i] if i < len(vols) else 0
            amount = amounts[i] if i < len(amounts) else 0
            
            change = close_px - pre_close if pre_close else 0
            pct_chg = (change / pre_close * 100) if pre_close else 0
            
            records.append({
                'symbol_code': symbol_code,
                'trade_date': str(date_str).replace('-', ''),
                'open': open_px,
                'high': high_px,
                'low': low_px,
                'close': close_px,
                'pre_close': pre_close,
                'change': round(change, 4),
                'pct_chg': round(pct_chg, 4),
                'vol': vol,
                'amount': amount
            })
            
        df = pd.DataFrame(records)
        return df

    def limit_list(self, trade_date='', symbol_code='', fields=''):
        """
        涨停板数据
        """
        if not trade_date:
            from datetime import datetime
            trade_date = datetime.now().strftime('%Y-%m-%d')
        else:
            if len(trade_date) == 8:
                trade_date = f"{trade_date[:4]}-{trade_date[4:6]}-{trade_date[6:]}"

        api_url = f"open/review/uplimit/stocks/{trade_date}"
        data = self.query(api_url)
        
        if not data:
            return pd.DataFrame()
            
        records = []
        for item in data:
            code = item.get('stock_code')
            if symbol_code and code not in symbol_code:
                continue
                
            records.append({
                'trade_date': item.get('date1', '').replace('-', ''),
                'symbol_code': code,
                'name': item.get('stock_name'),
                'close': item.get('fd_close'),
                'pct_chg': 10.0,
                'amount': item.get('amount'),
                'limit_amount': item.get('fd_max'),
                'float_mv': item.get('market_c'),
                'total_mv': item.get('market_c'),
                'turnover_ratio': 0,
                'limit_times': item.get('up_limit_keep_times'),
                'limit_status': item.get('up_limit_type'),
                'open_times': 0,
                'up_stat': item.get('up_limit_type'),
                'limit_reason': item.get('up_limit_desc')
            })
            
        df = pd.DataFrame(records)
        return df

    # --- TODO Interfaces ---
    
    def daily_basic(self, **kwargs):
        """每日指标 TODO"""
        return pd.DataFrame()

    def weekly(self, **kwargs):
        """周线行情 TODO"""
        return pd.DataFrame()

    def monthly(self, **kwargs):
        """月线行情 TODO"""
        return pd.DataFrame()

    def adj_factor(self, **kwargs):
        """复权因子 TODO"""
        return pd.DataFrame()

    def suspend_d(self, **kwargs):
        """停复牌信息 TODO"""
        return pd.DataFrame()

    def moneyflow(self, **kwargs):
        """个股资金流向 TODO"""
        # Potentially map to /stock/<stock_id>/moneyflow
        return pd.DataFrame()

    def income(self, **kwargs):
        """利润表 TODO"""
        return pd.DataFrame()

    def balancesheet(self, **kwargs):
        """资产负债表 TODO"""
        return pd.DataFrame()

    def cashflow(self, **kwargs):
        """现金流量表 TODO"""
        return pd.DataFrame()

    def forecast(self, **kwargs):
        """业绩预告 TODO"""
        return pd.DataFrame()

    def express(self, **kwargs):
        """业绩快报 TODO"""
        return pd.DataFrame()

    def dividend(self, **kwargs):
        """分红送转 TODO"""
        return pd.DataFrame()

    def fina_indicator(self, **kwargs):
        """财务指标数据 TODO"""
        return pd.DataFrame()

    def concept(self, **kwargs):
        """概念股分类 TODO"""
        return pd.DataFrame()

    def concept_detail(self, **kwargs):
        """概念股列表 TODO"""
        return pd.DataFrame()

    # --- Base Data (基础数据) ---
    def trade_days(self, start_date=None, end_date=None, ndays=None):
        """
        交易日历，返回交易日列表，数组形式，比如['2025-12-25', '2025-12-26', '2025-12-29', '2025-12-30', '2025-12-31']
        不传任何参数，返回最近10个交易日
        start_date: 开始日期，格式YYYY-MM-DD 和 end_date配合使用，返回这个区间的交易日
        end_date: 结束日期，格式YYYY-MM-DD，配合ndays使用返回最近ndays个交易日，或者配合start_date使用返回区间交易日
        ndays: 返回最近ndays个交易日，配合end_date使用返回end_date之前的ndays个交易日
        """
        api_url = "market/trade/days"
        params = {
            'day_start': start_date,
            'day_end': end_date,
            'days': ndays
        }
            
        data = self.query(api_url, params)
        return data or []

    def stock_company(self, **kwargs):
        """上市公司基本信息 TODO"""
        return pd.DataFrame()
        
    def stk_managers(self, **kwargs):
        """上市公司管理层 TODO"""
        return pd.DataFrame()
        
    def stk_rewards(self, **kwargs):
        """管理层薪酬 TODO"""
        return pd.DataFrame()
        
    def new_share(self, **kwargs):
        """IPO新股列表 TODO"""
        return pd.DataFrame()
        
    def hs_const(self, **kwargs):
        """沪深股通成份股 TODO"""
        return pd.DataFrame()
        
    def namechange(self, **kwargs):
        """股票曾用名 TODO"""
        return pd.DataFrame()

    # --- Market Data (行情数据 - Extended) ---
    def hsgt_top10(self, **kwargs):
        """沪深股通十大成交股 TODO"""
        return pd.DataFrame()
        
    def ggt_top10(self, **kwargs):
        """港股通十大成交股 TODO"""
        return pd.DataFrame()
        
    def ggt_daily(self, **kwargs):
        """港股通每日行情 TODO"""
        return pd.DataFrame()
    
    def moneyflow_hsgt(self, **kwargs):
        """沪深港通资金流向 TODO"""
        return pd.DataFrame()

    def stk_mins(self, symbol_code='', start_date='', end_date='', freq='1min'):
        """
        分钟行情
        TODO: zzzz-market-api currently does not expose a minute kline endpoint.
        """
        return pd.DataFrame()

    # --- Financial Data (财务数据 - Extended) ---
    def fina_audit(self, **kwargs):
        """财务审计意见 TODO"""
        return pd.DataFrame()
        
    def fina_mainbz(self, **kwargs):
        """主营业务构成 TODO"""
        return pd.DataFrame()
        
    def disclosure_date(self, **kwargs):
        """财报披露计划 TODO"""
        return pd.DataFrame()

    # --- Market Reference (市场参考数据) ---
    def margin(self, **kwargs):
        """融资融券交易汇总 TODO"""
        return pd.DataFrame()
        
    def margin_detail(self, **kwargs):
        """融资融券交易明细 TODO"""
        return pd.DataFrame()
        
    def top10_holders(self, **kwargs):
        """前十大股东 TODO"""
        return pd.DataFrame()
        
    def top10_floatholders(self, **kwargs):
        """前十大流通股东 TODO"""
        return pd.DataFrame()
        
    def top_list(self, **kwargs):
        """龙虎榜 TODO"""
        return pd.DataFrame()
        
    def block_trade(self, **kwargs):
        """大宗交易 TODO"""
        return pd.DataFrame()
        
    def stk_holdertrade(self, **kwargs):
        """董监高持股变动 TODO"""
        return pd.DataFrame()
        
    def pledge_stat(self, **kwargs):
        """股权质押统计 TODO"""
        return pd.DataFrame()
        
    def pledge_detail(self, **kwargs):
        """股权质押明细 TODO"""
        return pd.DataFrame()
        
    def repurchase(self, **kwargs):
        """股票回购 TODO"""
        return pd.DataFrame()

    # --- Index Data (指数数据) ---
    def index_basic(self, **kwargs):
        """指数基本信息 TODO"""
        return pd.DataFrame()
        
    def index_daily(self, **kwargs):
        """指数日线行情 TODO"""
        return pd.DataFrame()
        
    def index_weight(self, **kwargs):
        """指数成分和权重 TODO"""
        return pd.DataFrame()
        
    def index_dailybasic(self, **kwargs):
        """指数每日指标 TODO"""
        return pd.DataFrame()
        
    def index_classify(self, **kwargs):
        """申万行业分类 TODO"""
        return pd.DataFrame()
        
    def index_member(self, **kwargs):
        """申万行业成分 TODO"""
        return pd.DataFrame()

    # --- Fund Data (基金数据) ---
    def fund_basic(self, **kwargs):
        """公募基金列表 TODO"""
        return pd.DataFrame()
        
    def fund_net_value(self, **kwargs):
        """公募基金净值 TODO"""
        return pd.DataFrame()
        
    def fund_daily(self, **kwargs):
        """场内基金日线行情 TODO"""
        return pd.DataFrame()

    # --- News & Event (新闻/事件) ---
    def news(self, **kwargs):
        """新闻资讯 TODO"""
        return pd.DataFrame()

    def major_news(self, **kwargs):
        """大事提醒 TODO"""
        return pd.DataFrame()

    def cctv_news(self, **kwargs):
        """新闻联播 TODO"""
        return pd.DataFrame()

    # --- Convertible Bond (可转债) ---
    def cb_basic(self, **kwargs):
        """可转债基础信息 TODO"""
        return pd.DataFrame()

    def cb_issue(self, **kwargs):
        """可转债发行 TODO"""
        return pd.DataFrame()

    def cb_daily(self, **kwargs):
        """可转债行情 TODO"""
        return pd.DataFrame()

    def cb_call(self, **kwargs):
        """可转债赎回 TODO"""
        return pd.DataFrame()

    def cb_price(self, **kwargs):
        """可转债转股价 TODO"""
        return pd.DataFrame()

    # --- Futures (期货) ---
    def fut_basic(self, **kwargs):
        """期货合约信息 TODO"""
        return pd.DataFrame()

    def fut_daily(self, **kwargs):
        """期货日线行情 TODO"""
        return pd.DataFrame()

    def fut_holding(self, **kwargs):
        """期货持仓量 TODO"""
        return pd.DataFrame()

    def fut_settle(self, **kwargs):
        """期货结算参数 TODO"""
        return pd.DataFrame()

    # --- Options (期权) ---
    def opt_basic(self, **kwargs):
        """期权合约信息 TODO"""
        return pd.DataFrame()

    def opt_daily(self, **kwargs):
        """期权日线行情 TODO"""
        return pd.DataFrame()

    # --- FX (外汇) ---
    def fx_daily(self, **kwargs):
        """外汇日线行情 TODO"""
        return pd.DataFrame()
        
    def fx_ob_basic(self, **kwargs):
        """外汇基础信息 TODO"""
        return pd.DataFrame()

    # --- HK/US Stocks (港/美股) ---
    def hk_basic(self, **kwargs):
        """港股列表 TODO"""
        return pd.DataFrame()

    def hk_tradecal(self, **kwargs):
        """港股交易日历 TODO"""
        return pd.DataFrame()

    def us_basic(self, **kwargs):
        """美股列表 TODO"""
        return pd.DataFrame()

    def us_daily(self, **kwargs):
        """美股日线行情 TODO"""
        return pd.DataFrame()

    def us_tradecal(self, **kwargs):
        """美股交易日历 TODO"""
        return pd.DataFrame()

    # --- Macro/Interest (宏观/利率) ---
    def libor(self, **kwargs):
        """Libor利率 TODO"""
        return pd.DataFrame()

    def shibor(self, **kwargs):
        """Shibor利率 TODO"""
        return pd.DataFrame()
        
    def hibor(self, **kwargs):
        """Hibor利率 TODO"""
        return pd.DataFrame()

    def cn_gdp(self, **kwargs):
        """中国GDP TODO"""
        return pd.DataFrame()
        
    def cn_cpi(self, **kwargs):
        """中国CPI TODO"""
        return pd.DataFrame()
        
    def cn_ppi(self, **kwargs):
        """中国PPI TODO"""
        return pd.DataFrame()
        
    def cn_m(self, **kwargs):
        """中国货币供应量 TODO"""
        return pd.DataFrame()

    def us_tycr(self, **kwargs):
        """美国国债收益率 TODO"""
        return pd.DataFrame()

    # --- Fund Extended (基金扩展) ---
    def fund_manager(self, **kwargs):
        """基金经理 TODO"""
        return pd.DataFrame()
        
    def fund_share(self, **kwargs):
        """基金份额 TODO"""
        return pd.DataFrame()
        
    def fund_nav(self, **kwargs):
        """基金净值(Open) TODO"""
        return pd.DataFrame()
        
    def fund_portfolio(self, **kwargs):
        """基金持仓 TODO"""
        return pd.DataFrame()

    # --- Bond (债券) ---
    def bond_basic(self, **kwargs):
        """债券列表 TODO"""
        return pd.DataFrame()
        
    def bond_issue(self, **kwargs):
        """债券发行 TODO"""
        return pd.DataFrame()
        
    def bond_daily(self, **kwargs):
        """债券行情 TODO"""
        return pd.DataFrame()
        
    def bond_blk(self, **kwargs):
        """债券大宗交易 TODO"""
        return pd.DataFrame()

    # --- Stock Extended (股票扩展) ---
    def stk_surv(self, **kwargs):
        """机构调研 TODO"""
        return pd.DataFrame()
        
    def broker_recommend(self, **kwargs):
        """券商推荐 TODO"""
        return pd.DataFrame()
        
    def hk_hold(self, **kwargs):
        """沪深港股通持股 TODO"""
        return pd.DataFrame()

    def stk_limit(self, **kwargs):
        """每日涨跌停价格 TODO"""
        return pd.DataFrame()

    def bak_daily(self, **kwargs):
        """备用行情 TODO"""
        return pd.DataFrame()

    def bak_basic(self, **kwargs):
        """备用基础信息 TODO"""
        return pd.DataFrame()

    # --- Index Extended ---
    def index_global(self, **kwargs):
        """国际指数 TODO"""
        return pd.DataFrame()
        
    def index_monthly(self, **kwargs):
        """指数月线 TODO"""
        return pd.DataFrame()
        
    def index_weekly(self, **kwargs):
        """指数周线 TODO"""
        return pd.DataFrame()
        
    # --- Futures Extended ---
    def fut_weekly(self, **kwargs):
        """期货周线 TODO"""
        return pd.DataFrame()
        
    def fut_monthly(self, **kwargs):
        """期货月线 TODO"""
        return pd.DataFrame()


