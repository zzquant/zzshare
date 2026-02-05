# data_api.pyi
from typing import Any, Dict, List, Optional

from pandas import DataFrame


class DataApi:
    def __init__(
        self,
        token: str = ...,
        timeout: int = ...,
        http_url: str = ...
    ) -> None: ...

    def query(self, path: str, params: Optional[Dict[str, Any]] = None) -> Any: ...

    # ───────────── 以下为 IDE 补全用的显式签名 ─────────────

    def uplimit_hot(
        self,
        date1: str,
        board: Optional[str] = None
    ) -> Optional[Dict]: ...

    def uplimit_stocks(self, date1: str) -> Dict[str, Dict]: ...

    def market_plate_stocks(
        self,
        plate_code: str,
        date1: str,
        is_real: int = 1,
        limit: int = 50
    ) -> Any: ...

    def market_plate(
        self,
        date1: str,
        limit: int = 3
    ) -> Any: ...

    def market_sentiment(
        self,
        date1: str,
        date2: Optional[str] = None
    ) -> Any: ...

    def market_hot_sentiment(
        self,
        date1: str,
        date2: Optional[str] = None
    ) -> Any: ...

    def ths_hot_top(
        self,
        date1: str,
        top_n: int = 100
    ) -> Any: ...

    def stock_ths_hot(
        self,
        code: str,
        date1: str
    ) -> Any: ...

    def market_style(self, date1: str) -> Any: ...

    def open_sentiment_data(
        self,
        date1: str,
        date2: Optional[str] = None
    ) -> Any: ...

    def daily(self, code: str, date1: Optional[str] = None, date2: Optional[str] = None) -> DataFrame: ...

    def trade_days(self, day_start: Optional[str] = None, day_end: Optional[str] = None, days: int = None) -> Any: ...

    def sentiment_market_hot_day(self, date: str) -> Any: ...

    def sentiment_trend(
        self,
        model: int,
        date1: Optional[str] = None
    ) -> Any: ...

    def sentiment_trend_range(
        self,
        model: int,
        date1: Optional[str] = None,
        date2: Optional[str] = None
    ) -> Any: ...

    def review_uplimit_reason(
        self,
        date1: Optional[str] = None,
        group: Optional[int] = 1,
        page: Optional[int] = None,
        page_size: Optional[int] = None
    ) -> Any: ...

    def review_uplimit_hot_open(
        self,
        date1: Optional[str] = None,
        date2: Optional[str] = None,
        board: Optional[str] = None,
        limit: Optional[int] = None
    ) -> Any: ...

    def stock_uplimit_reason(
        self,
        stock_code: str,
        date: Optional[str] = None
    ) -> Any: ...

    def stock_uplimit_reason_history(
        self,
        stock_code: str,
        page: int = 1,
        pageSize: int = 10
    ) -> Any: ...

    def review_uplimit_reason_open(
        self,
        date1: Optional[str] = None
    ) -> Any: ...

    def stock_info(
        self,
        stock_id: str,
        info_type: int
    ) -> Any: ...

    # ================== 新增接口类型提示 ==================
    
    # 龙虎榜数据
    def lhb_list(self, date1: str) -> Any: ...
    
    def lhb_detail(self, date1: str, stock_code: str) -> Any: ...
    
    def lhb_stock_history(
        self,
        stock_code: str,
        trader_name: Optional[str] = None
    ) -> Any: ...
    
    def lhb_trader_history(
        self,
        trader_name: Optional[str] = None,
        trader_id: Optional[str] = None,
        stock_code: Optional[str] = None,
        page: int = 1,
        per_page: int = 20
    ) -> Any: ...
    
    # 板块数据
    def plates_list(self, plate_type: int) -> Any: ...
    
    def plates_rank(
        self,
        plate_type: int,
        date1: str,
        limit: int = 10
    ) -> Any: ...
    
    def plates_trend(
        self,
        plate_type: int,
        plate_code: str,
        day_start: str,
        day_end: str
    ) -> Any: ...
    
    def plates_stocks(
        self,
        plate_type: int,
        plate_code: str,
        date: Optional[str] = None
    ) -> Any: ...
    
    # 涨跌分布与情绪
    def updown_distribution(self, date1: str) -> Any: ...
    
    def uplimit_trend(self, date1: str) -> Any: ...
    
    def sentiment_hot_day(
        self,
        index: int = 0,
        st: int = 100
    ) -> Any: ...
    
    def sentiment_level(self, date: str) -> Any: ...
    
    def sentiment_bull_data(
        self,
        date1: str,
        date2: Optional[str] = None
    ) -> Any: ...
    
    # 行情实时数据
    def market_real(self, symbols: str) -> Any: ...
    
    def stock_moneyflow(
        self,
        stock_id: str,
        m_type: Optional[str] = None
    ) -> Any: ...
    
    def market_mf(
        self,
        stock: str,
        date: str,
        wm: int = 0,
        default_v: int = 0
    ) -> Any: ...
    
    # 涨停市值统计
    def uplimit_market_value(
        self,
        date1: str,
        date2: Optional[str] = None
    ) -> Any: ...
    
    # 市场TopN情绪
    def sentiment_market_top_n(
        self,
        modal_id: int = 1,
        date1: Optional[str] = None,
        date2: Optional[str] = None
    ) -> Any: ...
    
    # 异动数据
    def movement_alerts(
        self,
        date1: str,
        type: int = 0,
        limit: int = 200,
        is_real: int = 1
    ) -> Any: ...
    
    # 监控数据
    def zdjk_get(
        self,
        date1: str,
        date2: Optional[str] = None
    ) -> Any: ...