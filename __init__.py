
from .client import DataApi

class ProAPI:
    def __init__(self, token=''):
        self.api = DataApi(token)
    
    def query(self, api_name, fields='', **kwargs):
        return self.api.query(api_name, kwargs)
        
    def stock_basic(self, **kwargs): return self.api.stock_basic(**kwargs)
    def daily(self, **kwargs): return self.api.daily(**kwargs)
    def limit_list(self, **kwargs): return self.api.limit_list(**kwargs)
    
    def daily_basic(self, **kwargs): return self.api.daily_basic(**kwargs)
    def weekly(self, **kwargs): return self.api.weekly(**kwargs)
    def monthly(self, **kwargs): return self.api.monthly(**kwargs)
    def adj_factor(self, **kwargs): return self.api.adj_factor(**kwargs)
    def suspend_d(self, **kwargs): return self.api.suspend_d(**kwargs)
    def moneyflow(self, **kwargs): return self.api.moneyflow(**kwargs)
    def income(self, **kwargs): return self.api.income(**kwargs)
    def balancesheet(self, **kwargs): return self.api.balancesheet(**kwargs)
    def cashflow(self, **kwargs): return self.api.cashflow(**kwargs)
    def forecast(self, **kwargs): return self.api.forecast(**kwargs)
    def express(self, **kwargs): return self.api.express(**kwargs)
    def dividend(self, **kwargs): return self.api.dividend(**kwargs)
    def fina_indicator(self, **kwargs): return self.api.fina_indicator(**kwargs)
    def concept(self, **kwargs): return self.api.concept(**kwargs)
    def concept_detail(self, **kwargs): return self.api.concept_detail(**kwargs)

    # --- Base Data ---
    def trade_days(self, **kwargs): return self.api.trade_days(**kwargs)
    def stock_company(self, **kwargs): return self.api.stock_company(**kwargs)
    def stk_managers(self, **kwargs): return self.api.stk_managers(**kwargs)
    def stk_rewards(self, **kwargs): return self.api.stk_rewards(**kwargs)
    def new_share(self, **kwargs): return self.api.new_share(**kwargs)
    def hs_const(self, **kwargs): return self.api.hs_const(**kwargs)
    def namechange(self, **kwargs): return self.api.namechange(**kwargs)

    # --- Market Data ---
    def hsgt_top10(self, **kwargs): return self.api.hsgt_top10(**kwargs)
    def ggt_top10(self, **kwargs): return self.api.ggt_top10(**kwargs)
    def ggt_daily(self, **kwargs): return self.api.ggt_daily(**kwargs)
    def moneyflow_hsgt(self, **kwargs): return self.api.moneyflow_hsgt(**kwargs)
    def moneyflow(self, **kwargs): return self.api.moneyflow(**kwargs)
    def stk_mins(self, **kwargs): return self.api.stk_mins(**kwargs)

    # --- Financial Data ---
    def fina_audit(self, **kwargs): return self.api.fina_audit(**kwargs)
    def fina_mainbz(self, **kwargs): return self.api.fina_mainbz(**kwargs)
    def disclosure_date(self, **kwargs): return self.api.disclosure_date(**kwargs)

    # --- Market Reference ---
    def margin(self, **kwargs): return self.api.margin(**kwargs)
    def margin_detail(self, **kwargs): return self.api.margin_detail(**kwargs)
    def top10_holders(self, **kwargs): return self.api.top10_holders(**kwargs)
    def top10_floatholders(self, **kwargs): return self.api.top10_floatholders(**kwargs)
    def top_list(self, **kwargs): return self.api.top_list(**kwargs)
    def block_trade(self, **kwargs): return self.api.block_trade(**kwargs)
    def stk_holdertrade(self, **kwargs): return self.api.stk_holdertrade(**kwargs)
    def pledge_stat(self, **kwargs): return self.api.pledge_stat(**kwargs)
    def pledge_detail(self, **kwargs): return self.api.pledge_detail(**kwargs)
    def repurchase(self, **kwargs): return self.api.repurchase(**kwargs)

    # --- Index Data ---
    def index_basic(self, **kwargs): return self.api.index_basic(**kwargs)
    def index_daily(self, **kwargs): return self.api.index_daily(**kwargs)
    def index_weight(self, **kwargs): return self.api.index_weight(**kwargs)
    def index_dailybasic(self, **kwargs): return self.api.index_dailybasic(**kwargs)
    def index_classify(self, **kwargs): return self.api.index_classify(**kwargs)
    def index_member(self, **kwargs): return self.api.index_member(**kwargs)

    # --- Fund Data ---
    def fund_basic(self, **kwargs): return self.api.fund_basic(**kwargs)
    def fund_net_value(self, **kwargs): return self.api.fund_net_value(**kwargs)
    def fund_daily(self, **kwargs): return self.api.fund_daily(**kwargs)

    # --- News & Event ---
    def news(self, **kwargs): return self.api.news(**kwargs)
    def major_news(self, **kwargs): return self.api.major_news(**kwargs)
    def cctv_news(self, **kwargs): return self.api.cctv_news(**kwargs)

    # --- Convertible Bond ---
    def cb_basic(self, **kwargs): return self.api.cb_basic(**kwargs)
    def cb_issue(self, **kwargs): return self.api.cb_issue(**kwargs)
    def cb_daily(self, **kwargs): return self.api.cb_daily(**kwargs)
    def cb_call(self, **kwargs): return self.api.cb_call(**kwargs)
    def cb_price(self, **kwargs): return self.api.cb_price(**kwargs)

    # --- Futures ---
    def fut_basic(self, **kwargs): return self.api.fut_basic(**kwargs)
    def fut_daily(self, **kwargs): return self.api.fut_daily(**kwargs)
    def fut_holding(self, **kwargs): return self.api.fut_holding(**kwargs)
    def fut_settle(self, **kwargs): return self.api.fut_settle(**kwargs)

    # --- Options ---
    def opt_basic(self, **kwargs): return self.api.opt_basic(**kwargs)
    def opt_daily(self, **kwargs): return self.api.opt_daily(**kwargs)

    # --- FX ---
    def fx_daily(self, **kwargs): return self.api.fx_daily(**kwargs)
    def fx_ob_basic(self, **kwargs): return self.api.fx_ob_basic(**kwargs)

    # --- HK/US Stocks ---
    def hk_basic(self, **kwargs): return self.api.hk_basic(**kwargs)
    def hk_tradecal(self, **kwargs): return self.api.hk_tradecal(**kwargs)
    def us_basic(self, **kwargs): return self.api.us_basic(**kwargs)
    def us_daily(self, **kwargs): return self.api.us_daily(**kwargs)
    def us_tradecal(self, **kwargs): return self.api.us_tradecal(**kwargs)

    # --- Macro/Interest ---
    def libor(self, **kwargs): return self.api.libor(**kwargs)
    def shibor(self, **kwargs): return self.api.shibor(**kwargs)
    def hibor(self, **kwargs): return self.api.hibor(**kwargs)
    def cn_gdp(self, **kwargs): return self.api.cn_gdp(**kwargs)
    def cn_cpi(self, **kwargs): return self.api.cn_cpi(**kwargs)
    def cn_ppi(self, **kwargs): return self.api.cn_ppi(**kwargs)
    def cn_m(self, **kwargs): return self.api.cn_m(**kwargs)
    def us_tycr(self, **kwargs): return self.api.us_tycr(**kwargs)

    # --- Fund Extended ---
    def fund_manager(self, **kwargs): return self.api.fund_manager(**kwargs)
    def fund_share(self, **kwargs): return self.api.fund_share(**kwargs)
    def fund_nav(self, **kwargs): return self.api.fund_nav(**kwargs)
    def fund_portfolio(self, **kwargs): return self.api.fund_portfolio(**kwargs)

    # --- Bond ---
    def bond_basic(self, **kwargs): return self.api.bond_basic(**kwargs)
    def bond_issue(self, **kwargs): return self.api.bond_issue(**kwargs)
    def bond_daily(self, **kwargs): return self.api.bond_daily(**kwargs)
    def bond_blk(self, **kwargs): return self.api.bond_blk(**kwargs)

    # --- Stock Extended ---
    def stk_surv(self, **kwargs): return self.api.stk_surv(**kwargs)
    def broker_recommend(self, **kwargs): return self.api.broker_recommend(**kwargs)
    def hk_hold(self, **kwargs): return self.api.hk_hold(**kwargs)
    def stk_limit(self, **kwargs): return self.api.stk_limit(**kwargs)
    def daily_basic(self, **kwargs): return self.api.daily_basic(**kwargs)
    def bak_daily(self, **kwargs): return self.api.bak_daily(**kwargs)
    def bak_basic(self, **kwargs): return self.api.bak_basic(**kwargs)
    
    # --- Index/Futures Extended ---
    def index_global(self, **kwargs): return self.api.index_global(**kwargs)
    def index_monthly(self, **kwargs): return self.api.index_monthly(**kwargs)
    def index_weekly(self, **kwargs): return self.api.index_weekly(**kwargs)
    def fut_weekly(self, **kwargs): return self.api.fut_weekly(**kwargs)
    def fut_monthly(self, **kwargs): return self.api.fut_monthly(**kwargs)


def pro_api(token=''):
    """
    Initialize Pro API
    """
    return ProAPI(token)

def pro_bar(symbol_code='', start_date='', end_date='', freq='D', asset='E', 
           exchange='', adj=None, ma=[], factor=None, contract_type='', **kwargs):
    """
    BAR数据
    TODO: Integrate with daily/stk_mins and adjustment factors
    """
    import pandas as pd
    return pd.DataFrame()
