# data_api.pyi
from typing import Any, Dict, List, Optional

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

    def market_sentiment_hot_day(self, date1: str) -> Optional[List[Dict]]: ...

    def market_style(self, date1: str) -> Any: ...

    def open_sentiment_data(
        self,
        date1: str,
        date2: Optional[str] = None
    ) -> Any: ...