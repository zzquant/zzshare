from functools import partial
import requests
from typing import Any, Optional, Dict, Callable, List, Tuple, Union
import pandas as pd

from zzshare.core import BaseDataApi
from zzshare.utils import kline_data_to_df


class DataApi(BaseDataApi):
    def __init__(self, token: str = '', timeout: int = 10, http_url: str = 'https://api.zizizaizai.com'):
        super().__init__(token, timeout, http_url)

    SHORTCUTS = {
        # Daily
        "uplimit_hot": (
            "open/review/uplimit/hot",
            ["date1", "board"],
            None
        ),
        "uplimit_stocks": (
            "open/review/uplimit/stocks/{date1}",
            ["date1"],
            None
        ),
        # Sentiment Data
        "market_plate_stocks": (
            "market/plates/17/{plate_code}/stocks/rank",
            ["plate_code", "date1", "is_real", "limit"],
            None
        ),
        "market_plate": (
            "market/plates/17/rank",
            ["date1", "limit"],
            None
        ),
        "market_sentiment": (
            "v2/api/sentiment/kline/day/0",
            ["date1", "date2"],
            None
        ),
        "market_hot_sentiment": (
            "v2/api/sentiment/kline/day/20",
            ["date1", "date2"],
            None
        ),
        "market_style": (
            "v2/api/timing/market/style",
            ["date1"],
            None
        ),
        "open_sentiment_data": (
            "open/sentiment/data",
            ["date1", "date2"],
            None
        ),
        # Kline
        "daily": (
            "open/kline/d/{code}",
            ["code", "date1", "date2"],
            kline_data_to_df
        ),
        # Base Data
        "trade_days": (
            "market/trade/days",
            ["day_start", "day_end", "days"],
            None
        ),
        # Third Party
        "ths_hot_top": (
            "open/sentiment/media/ths2/top",
            ["date1", "top_n"],
            None
        ),
        "stock_ths_hot": (
            "v2/api/sentiment/media/ths/symbol/{code}",
            ["code", "date1"],
            None
        ),
        "sentiment_market_hot_day": (
            "v3/api/sentiment/market/hot/day",
            ["date"],
            None
        ),
        "sentiment_trend": (
            "v3/api/sentiment/trend/{model}",
            ["model", "date1"],
            None
        ),
        "sentiment_trend_range": (
            "v3/api/sentiment/trend/{model}/range",
            ["model", "date1", "date2"],
            None
        ),
        "review_uplimit_reason": (
            "v3/api/review/uplimit/reason",
            ["date1", "group", "page", "page_size"],
            None
        ),
        "review_uplimit_hot_open": (
            "v3/open/review/uplimit/hot",
            ["date1", "date2", "board", "limit"],
            None
        ),
        "stock_uplimit_reason": (
            "v3/open/stock/uplimit/reason/{stock_code}",
            ["stock_code", "date"],
            None
        ),
        "stock_uplimit_reason_history": (
            "v3/open/stock/uplimit/reason/history/{stock_code}", ["stock_code", "page", "pageSize"], None),
        "review_uplimit_reason_open": (
            "v3/open/review/uplimit/reason",
            ["date1"],
            None
        ),
        "stock_info": (
            "v3/open/stock/info",
            ["stock_id", "info_type"],
            None
        ),
        # ================== 新增接口 ==================
        # 龙虎榜数据
        "lhb_list": (
            "market/lhb/list",
            ["date1"],
            None
        ),
        "lhb_detail": (
            "market/lhb/detail",
            ["date1", "stock_code"],
            None
        ),
        "lhb_stock_history": (
            "market/lhb/stock/history",
            ["stock_code", "trader_name"],
            None
        ),
        "lhb_trader_history": (
            "market/lhb/trader/history",
            ["trader_name", "trader_id", "stock_code", "page", "per_page"],
            None
        ),
        # 板块数据
        "plates_list": (
            "market/plates/{plate_type}",
            ["plate_type"],
            None
        ),
        "plates_rank": (
            "market/plates/{plate_type}/rank",
            ["plate_type", "date1", "limit"],
            None
        ),
        "plates_trend": (
            "market/plates/{plate_type}/trend",
            ["plate_type", "plate_code", "day_start", "day_end"],
            None
        ),
        "plates_stocks": (
            "market/plates/{plate_type}/{plate_code}/stocks",
            ["plate_type", "plate_code", "date"],
            None
        ),
        # 涨跌分布与情绪
        "updown_distribution": (
            "open/sentiment/updown/disctribution",
            ["date1"],
            None
        ),
        "uplimit_trend": (
            "open/sentiment/uplimit/trend",
            ["date1"],
            None
        ),
        "sentiment_hot_day": (
            "open/sentiment/hot/day",
            ["index", "st"],
            None
        ),
        "sentiment_level": (
            "open/sentiment/level",
            ["date"],
            None
        ),
        "sentiment_bull_data": (
            "open/sentiment/bull/data",
            ["date1", "date2"],
            None
        ),
        # 行情实时数据
        "market_real": (
            "open/market/real",
            ["symbols"],
            None
        ),
        "stock_moneyflow": (
            "open/stock/{stock_id}/moneyflow",
            ["stock_id", "m_type"],
            None
        ),
        "market_mf": (
            "open/market/mf",
            ["stock", "date", "wm", "default_v"],
            None
        ),
        # 涨停市值统计
        "uplimit_market_value": (
            "v2/api/uplimit/market/value",
            ["date1", "date2"],
            None
        ),
        # 市场TopN情绪
        "sentiment_market_top_n": (
            "v2/api/sentiment/market/top/n",
            ["modal_id", "date1", "date2"],
            None
        ),
        # 异动数据
        "movement_alerts": (
            "market/movement/alerts",
            ["date1", "type", "limit", "is_real"],
            None
        ),
        # 监控数据
        "zdjk_get": (
            "open/zdjk/get",
            ["date1", "date2"],
            None
        ),
    }

    def _register_shortcuts(self):
        """根据 SHORTCUTS 表动态生成方法"""
        for name, (path_template, param_names, post_process) in self.SHORTCUTS.items():
            if name == "daily":
                continue
            def make_method(
                    template: str = path_template,
                    params_list: List[str] = param_names,
                    processor: Optional[Callable[[Optional[Dict]], Any]] = post_process
            ):
                def shortcut_method(**kwargs) -> Any:
                    path = template
                    # 先处理路径参数：从 kwargs 中 pop 并替换 {xxx}
                    for param in params_list:
                        placeholder = f"{{{param}}}"
                        if placeholder in path:
                            if param not in kwargs:
                                raise ValueError(f"缺少路径参数 '{param}' for {name}")
                            value = kwargs.pop(param)
                            path = path.replace(placeholder, str(value))

                    # 剩下的 kwargs 作为 query 参数
                    data = self._query(path.lstrip('/'), params=kwargs)

                    # 后处理
                    if processor:
                        return processor(data)
                    return data

                # 绑定方法名和文档
                shortcut_method.__name__ = name
                shortcut_method.__doc__ = (
                    f"快捷调用：{template}\n"
                    f"参数：{', '.join(params_list)}（路径参数会自动替换）\n"
                    f"后处理：{processor.__name__ if processor else '无'}"
                )
                setattr(self, name, shortcut_method)

            make_method()

    @staticmethod
    def _normalize_symbol(symbol: str) -> str:
        return symbol.split(".")[0] if "." in symbol else symbol

    @staticmethod
    def _to_tushare_ts_code(symbol: str) -> str:
        normalized = symbol.strip().upper()
        if "." in normalized:
            code, suffix = normalized.split(".", 1)
            suffix_map = {
                "SS": "SH",
                "SH": "SH",
                "XSHG": "SH",
                "SZ": "SZ",
                "XSHE": "SZ",
                "BJ": "BJ",
                "BSE": "BJ",
            }
            return f"{code}.{suffix_map.get(suffix, suffix)}"
        if normalized.startswith(("6", "5")):
            return f"{normalized}.SH"
        if normalized.startswith(("0", "3")):
            return f"{normalized}.SZ"
        if normalized.startswith(("8", "4", "2", "9")):
            return f"{normalized}.BJ"
        return normalized

    @staticmethod
    def _to_tushare_exchange(symbol: str) -> str:
        code = symbol.split(".")[0] if "." in symbol else symbol
        if code.startswith(("6", "5")):
            return "SSE"
        if code.startswith(("0", "3")):
            return "SZSE"
        if code.startswith(("8", "4", "2", "9")):
            return "BSE"
        return ""

    @staticmethod
    def _to_backend_exchange(exchange: Optional[str]) -> Optional[str]:
        if not exchange:
            return None
        mapping = {
            "SSE": "SS",
            "SZSE": "SZ",
            "BSE": "BJ",
            "SH": "SS",
            "SZ": "SZ",
            "BJ": "BJ",
            "GEM": "GEM",
            "KSH": "KSH",
            "STAR": "KSH",
            "SS": "SS",
            "ALL": "ALL",
        }
        return mapping.get(exchange.upper())

    def daily(
        self,
        ts_code: Optional[str] = None,
        trade_date: Optional[str] = None,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        code: Optional[str] = None,
        date1: Optional[str] = None,
        date2: Optional[str] = None,
        fields: Optional[str] = None,
        **kwargs: Any
    ):
        use_code = ts_code or code
        if not use_code:
            raise ValueError("ts_code 或 code 不能为空")
        normalized_symbol = self._normalize_symbol(use_code)
        use_date1 = date1 or trade_date or start_date
        use_date2 = date2 or trade_date or end_date

        params: Dict[str, Any] = dict(kwargs)
        if use_date1:
            params["date1"] = use_date1
        if use_date2:
            params["date2"] = use_date2

        data = self._query(f"open/kline/d/{normalized_symbol}", params=params)
        df = kline_data_to_df(data)

        if df.empty:
            default_columns = [
                "ts_code", "trade_date", "open", "high", "low", "close",
                "pre_close", "change", "pct_chg", "vol", "amount"
            ]
            return df.reindex(columns=default_columns)

        df["ts_code"] = self._to_tushare_ts_code(use_code)
        ordered_columns = [
            "ts_code", "trade_date", "open", "high", "low", "close",
            "pre_close", "change", "pct_chg", "vol", "amount"
        ]
        df = df[[col for col in ordered_columns if col in df.columns]]
        df = df.sort_values(by="trade_date", ascending=False).reset_index(drop=True)

        if fields:
            requested_fields = [field.strip() for field in fields.split(",") if field.strip()]
            selected_fields = [field for field in requested_fields if field in df.columns]
            if selected_fields:
                return df[selected_fields]
            return df.iloc[:, 0:0]

        return df

    def stock_basic(
        self,
        ts_code: Optional[str] = None,
        exchange: Optional[str] = None,
        list_status: str = "L",
        is_hs: Optional[str] = None,
        fields: Optional[str] = None,
        name: Optional[str] = None,
        **kwargs: Any
    ):
        requested_status = (list_status or "L").upper()
        if requested_status not in {"L", "D", "P"}:
            raise ValueError("list_status 仅支持 L/D/P")

        backend_exchange = self._to_backend_exchange(exchange)
        if exchange and backend_exchange is None:
            raise ValueError("exchange 仅支持 SSE/SZSE/BSE/SH/SZ/BJ/GEM/KSH/STAR/SS/ALL")

        if requested_status == "P":
            df_empty = pd.DataFrame(columns=[
                "ts_code", "symbol", "name", "area", "industry", "fullname", "enname",
                "cnspell", "market", "exchange", "curr_type", "list_status",
                "list_date", "delist_date", "is_hs"
            ])
            if fields:
                requested_fields = [field.strip() for field in fields.split(",") if field.strip()]
                selected_fields = [field for field in requested_fields if field in df_empty.columns]
                if selected_fields:
                    return df_empty[selected_fields]
                return df_empty.iloc[:, 0:0]
            return df_empty

        query_status = requested_status if requested_status in {"L", "D"} else "ALL"
        exchange_list = [backend_exchange] if backend_exchange else ["SS", "KSH", "SZ", "GEM", "BJ"]
        rows: List[Dict[str, Any]] = []
        for ex in exchange_list:
            data = self._query(
                "v3/open/stocks/list",
                params={
                    "exchange": ex,
                    "list_status": query_status,
                    "format": "records"
                }
            )
            if isinstance(data, dict):
                batch = data.get("list") or []
                if isinstance(batch, list):
                    rows.extend(batch)

        normalized_codes: Optional[List[str]] = None
        if ts_code:
            normalized_codes = [self._normalize_symbol(item.strip()) for item in ts_code.split(",") if item.strip()]

        result_rows: List[Dict[str, Any]] = []
        for row in rows:
            code = str(row.get("code", "")).strip()
            if not code:
                continue
            if normalized_codes is not None and code not in normalized_codes:
                continue
            row_name = str(row.get("name", "")).strip()
            if name and name not in row_name:
                continue

            ex_name = self._to_tushare_exchange(code)
            type_code = str(row.get("type_code", "")).upper()
            market_name = "创业板" if type_code == "GEM" else "科创板" if "KSH" in type_code else ""
            result_rows.append({
                "ts_code": self._to_tushare_ts_code(code),
                "symbol": code,
                "name": row_name,
                "area": "",
                "industry": "",
                "fullname": row_name,
                "enname": "",
                "cnspell": "",
                "market": market_name,
                "exchange": ex_name,
                "curr_type": "CNY",
                "list_status": str(row.get("list_status", query_status)).upper(),
                "list_date": "",
                "delist_date": "",
                "is_hs": "",
            })

        df = pd.DataFrame(result_rows)
        ordered_columns = [
            "ts_code", "symbol", "name", "area", "industry", "fullname", "enname",
            "cnspell", "market", "exchange", "curr_type", "list_status",
            "list_date", "delist_date", "is_hs"
        ]
        if df.empty:
            df = pd.DataFrame(columns=ordered_columns)
        else:
            df = df[ordered_columns].drop_duplicates(subset=["ts_code"]).reset_index(drop=True)

        if is_hs:
            flag = is_hs.upper()
            if flag in {"H", "S"}:
                df = df.iloc[0:0]

        if fields:
            requested_fields = [field.strip() for field in fields.split(",") if field.strip()]
            selected_fields = [field for field in requested_fields if field in df.columns]
            if selected_fields:
                return df[selected_fields]
            return df.iloc[:, 0:0]

        return df
