import requests
from typing import Any, Optional, Dict, Callable, List, Union
import pandas as pd

from zzshare.core import BaseDataApi
from zzshare.utils import kline_data_to_df
from zzshare.logger import logger


class DataApi(BaseDataApi):
    def __init__(self, token: str = '', timeout: int = 10, http_url: str = 'https://api.zizizaizai.com'):
        super().__init__(token, timeout, http_url)

    SHORTCUTS = {
        # Daily
        "uplimit_hot": (
            "open/review/uplimit/hot",
            ["date1", "board"],
            None,
            "获取当日涨停热点板块及其连板梯队数据"
        ),
        "uplimit_stocks": (
            "open/review/uplimit/stocks/{date1}",
            ["date1"],
            None,
            "获取指定日期所有涨停股票的列表"
        ),
        # Sentiment Data
        "market_plate_stocks": (
            "market/plates/17/{plate_code}/stocks/rank",
            ["plate_code", "date1", "is_real", "limit"],
            None,
            "获取特定板块内的成分股涨跌幅排名"
        ),
        "market_plate": (
            "market/plates/17/rank",
            ["date1", "limit"],
            None,
            "获取全市场所有板块（行业/概念）的热度排名"
        ),
        "market_sentiment": (
            "v2/api/sentiment/kline/day/0",
            ["date1", "date2"],
            None,
            "综合市场情绪数据量化出来的K线数据"
        ),
        "market_hot_sentiment": (
            "v2/api/sentiment/kline/day/20",
            ["date1", "date2"],
            None,
            "市场热度情绪走势量化出来的K线数据"
        ),
        "market_style": (
            "v2/api/timing/market/style",
            ["date1"],
            None,
            "市场风格评估数据,适合什么风格的市场,量化出来的K线数据"
        ),
        "open_sentiment_data": (
            "open/sentiment/data",
            ["date1", "date2"],
            None,
            "多维情绪聚合数据接口"
        ),
        # Kline
        "daily": (
            "open/kline/d/{code}",
            ["code", "date1", "date2"],
            kline_data_to_df,
            "获取日线行情数据"
        ),
        # Base Data
        "trade_days": (
            "market/trade/days",
            ["day_start", "day_end", "days"],
            None,
            "查询 A 股交易日历（识别交易日与假期）"
        ),
        # Third Party
        "ths_hot_top": (
            "open/sentiment/media/ths2/top",
            ["date1", "top_n"],
            None,
            "获取同花顺热搜榜前 N 名龙头的实时排名"
        ),
        "stock_ths_hot": (
            "v2/api/sentiment/media/ths/symbol/{code}",
            ["code", "date1"],
            None,
            "查询特定股票在同花顺平台的热度趋势"
        ),
        "sentiment_market_hot_day": (
            "v3/api/sentiment/market/hot/day",
            ["date"],
            None,
            "每日市场核心热点数据统计"
        ),
        "sentiment_trend": (
            "v3/api/sentiment/trend/{model}",
            ["model", "date1"],
            None,
            "基于特定模型计算的市场情绪分时数据"
        ),
        "sentiment_trend_range": (
            "v3/api/sentiment/trend/{model}/range",
            ["model", "date1", "date2"],
            None,
            "区间市场情绪分时数据"
        ),
        "review_uplimit_reason": (
            "v3/api/review/uplimit/reason",
            ["date1", "group", "page", "page_size"],
            None,
            "全市场涨停复盘：包含个股具体的涨停原因与逻辑分析"
        ),
        "review_uplimit_hot_open": (
            "v3/open/review/uplimit/hot",
            ["date1", "date2", "board", "limit"],
            None,
            "开放版热点涨停分析" # ?
        ),
        "stock_uplimit_reason": (
            "v3/open/stock/uplimit/reason/{stock_code}",
            ["stock_code", "date"],
            None,
            "查询单只股票指定日期的涨停原因"
        ),
        "stock_uplimit_reason_history": (
            "v3/open/stock/uplimit/reason/history/{stock_code}", ["stock_code", "page", "pageSize"], None, "查询个股历史所有涨停记录及原因"),
        "review_uplimit_reason_open": (
            "v3/open/review/uplimit/reason",
            ["date1"],
            None,
            "指定日期全部涨停个股的涨停数据和原因汇总"
        ),
        "stock_info": (
            "v3/open/stock/info",
            ["stock_id", "info_type"],
            None,
            "获取股票的基础信息扩展字段"
        ),
        # 龙虎榜数据
        "lhb_list": (
            "market/lhb/list",
            ["date1"],
            None,
            "龙虎榜每日上榜股票概览列表"
        ),
        "lhb_detail": (
            "market/lhb/detail",
            ["date1", "stock_code"],
            None,
            "查询特定股票的龙虎榜席位买卖详情"
        ),
        "lhb_stock_history": (
            "market/lhb/stock/history",
            ["stock_code", "trader_name"],
            None,
            "查询个股或特定营业部的历史龙虎榜表现"
        ),
        "lhb_trader_history": (
            "market/lhb/trader/history",
            ["trader_name", "trader_id", "stock_code", "page", "per_page"],
            None,
            "龙虎榜知名游资/席位的历史交易轨迹"
        ),
        # 板块数据
        "plates_list": (
            "market/plates/{plate_type}",
            ["plate_type"],
            None,
            "获取指定类型（行业/概念/风格）的所有板块列表"
        ),
        "plates_rank": (
            "market/plates/{plate_type}/rank",
            ["plate_type", "date1", "limit"],
            None,
            "板块涨跌幅/综合热度实时排名"
        ),
        "plates_trend": (
            "market/plates/{plate_type}/trend",
            ["plate_type", "plate_code", "day_start", "day_end"],
            None,
            "指定板块的分时数据"
        ),
        "plates_stocks": (
            "market/plates/{plate_type}/{plate_code}/stocks",
            ["plate_type", "plate_code", "date"],
            None,
            "查询特定板块包含的所有个股详情"
        ),
        # 涨跌分布与情绪
        "updown_distribution": (
            "open/sentiment/updown/disctribution",
            ["date1"],
            None,
            "全市场每日上涨、下跌家数分布及涨停/跌停总数统计"
        ),
        "uplimit_trend": (
            "open/sentiment/uplimit/trend",
            ["date1"],
            None,
            "全市场涨停家数趋势及赚钱效应分析"
        ),
        "sentiment_hot_day": (
            "open/sentiment/hot/day",
            ["index", "st"],
            None,
            "市场每日核心人气热点排名"
        ),
        "sentiment_level": (
            "open/sentiment/level",
            ["date"],
            None,
            "整点市场情绪等级评估"
        ),
        "sentiment_bull_data": (
            "open/sentiment/bull/data",
            ["date1", "date2"],
            None,
            "多空情绪对比及牛市指标参考"
        ),
        # 行情实时数据
        # "stock_moneyflow": (
        #     "open/stock/{stock_id}/moneyflow",
        #     ["stock_id", "m_type"],
        #     None,
        #     "个股实时主力主力资金流向（超大单/大单等）"
        # ),
        # "market_mf": (
        #     "open/market/mf",
        #     ["stock", "date", "wm", "default_v"],
        #     None,
        #     "全量市场资金流分布概览"
        # ),
        # 涨停市值统计
        "uplimit_market_value": (
            "v2/api/uplimit/market/value",
            ["date1", "date2"],
            None,
            "基于市值的涨停板个股分布统计"
        ),
        # 市场TopN情绪
        # "sentiment_market_top_n": (
        #     "v2/api/sentiment/market/top/n",
        #     ["modal_id", "date1", "date2"],
        #     None,
        #     "市场最热的前 N 名热点概念动态跟踪"
        # ),
        # 异动数据
        "movement_alerts": (
            "market/movement/alerts",
            ["date1", "type", "limit", "is_real"],
            None,
            "沪深涨幅触发监管以及距离触发的空间"
        ),
        # 监控数据
        "zdjk_get": (
            "open/zdjk/get",
            ["date1", "date2"],
            None,
            "已经触发监管的股票列表"
        ),
    }

    def _register_shortcuts(self):
        """根据 SHORTCUTS 表动态生成方法"""
        for name, entry in self.SHORTCUTS.items():
            if name == "daily":
                continue
            
            # 支持旧的三元组或新的四元组
            if len(entry) == 3:
                path_template, param_names, post_process = entry
                description = f"快捷调用：{path_template}"
            else:
                path_template, param_names, post_process, description = entry

            def make_method(
                    template: str = path_template,
                    params_list: List[str] = param_names,
                    processor: Optional[Callable[[Optional[Dict]], Any]] = post_process,
                    desc: str = description
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
                    f"{desc}\n\n"
                    f"API路径：{template}\n"
                    f"参数：{', '.join(params_list)}（路径参数会自动替换）\n"
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

    def rt_k(self, ts_code: str = '', **kwargs: Any):
        """
        获取实时日线快照数据
        :param ts_code: 股票代码（支持多个用逗号隔开，或使用 3*.SZ 这样的通配符）
        :param fields: 当设为 'all' 时，返回扩展的高级量化字段。
        """
        params = {}
        if ts_code:
            params["ts_code"] = ts_code

        url = f"{self.http_url}/v3/market/kline/realtime"
        try:
            response = requests.get(url, params=params, headers=self.headers, timeout=self.timeout)
            response.raise_for_status()
            data = response.json().get("data", {}).get("list", [])
        except Exception as e:
            logger.exception(f"Request Error: {e}")
            data = []
        df = pd.DataFrame(data)

        base_cols = ['ts_code', 'name', 'pre_close', 'high', 'open', 'low', 'close', 'vol', 'amount', 'num', 'ask_price1', 'ask_volume1', 'bid_price1', 'bid_volume1']
        if df.empty:
            return pd.DataFrame(columns=base_cols)

        # 转换数字类型
        numeric_cols = [
            'pre_close', 'open', 'high', 'low', 'close', 'vol', 'amount', 'num',
            'ask_price1', 'ask_volume1', 'bid_price1', 'bid_volume1',
            'quote_rate', 'high_limit', 'low_limit', 'turnover_rate', 'market_value', 'circulation_value',
            'min5_chgpct', 'ttm_pe_rate', 'eps_ttm', 'auction_vol', 'auction_val', 'auction_px'
        ]
        for col in numeric_cols:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col], errors='coerce')

        fields = kwargs.get("fields", "")
        if fields == "all":
            # 扩展模式
            return df
        else:
            # 强兼容模式
            return df[base_cols]

    def daily(
        self,
        ts_code: Optional[str] = None,
        trade_date: Optional[str] = None,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        offset: Optional[int] = None,
        limit: Optional[int] = None,
        fields: Optional[str] = None,
        **kwargs: Any
    ):
        use_ts_code = self._to_tushare_ts_code(ts_code) if ts_code else None
        normalized_trade_date = trade_date.replace("-", "") if trade_date else None
        normalized_start = start_date.replace("-", "") if start_date else None
        normalized_end = end_date.replace("-", "") if end_date else None
        params: Dict[str, Any] = {}
        adj = str(kwargs.pop("adj", "")).lower()
        candle_mode = kwargs.pop("candle_mode", None)
        if candle_mode is None:
            if adj == "qfq":
                candle_mode = 1
            elif adj == "hfq":
                candle_mode = 2
            else:
                candle_mode = 0
        params["candle_mode"] = candle_mode

        if not use_ts_code:
            if not normalized_trade_date:
                raise ValueError("当 ts_code 为空时，trade_date 不能为空")
            params["trade_date"] = normalized_trade_date
            if offset is not None:
                params["offset"] = offset
            if limit is not None:
                params["limit"] = limit
            url = f"{self.http_url}/v3/market/kline/day"
        else:
            if normalized_trade_date:
                params["get_type"] = "range"
                params["start_date"] = normalized_trade_date
                params["end_date"] = normalized_trade_date
            else:
                params["get_type"] = "range"
                if normalized_start:
                    params["start_date"] = normalized_start
                if normalized_end:
                    params["end_date"] = normalized_end
            url = f"{self.http_url}/v3/market/kline/day/{use_ts_code}"

        params.update(kwargs)
        data: Optional[Union[Dict[str, Any], List[Any]]] = None
        try:
            res = requests.get(url, params=params, headers=self.headers, timeout=self.timeout)
            if res.status_code == 200:
                body = res.json()
                if isinstance(body, dict):
                    if body.get("code") == 200:
                        data = body.get("data")
                    elif "data" in body:
                        data = body.get("data")
                    else:
                        data = body
            elif res.status_code == 401:
                logger.error("Unauthorized. Please check your API token at https://quant.zizizaizai.com/me/profile")
            elif res.status_code == 429:
                logger.warning(f"Rate limit exceeded. {res.text}")
            else:
                logger.error(f"HTTP Error: {res.status_code} - {res.text}")
        except Exception as e:
            logger.exception(f"Request Error: {e}")
            data = None
        records: List[Dict[str, Any]] = []
        data_ts_code: Optional[str] = None
        if isinstance(data, list):
            records = [item for item in data if isinstance(item, dict)]
        elif isinstance(data, dict):
            data_ts_code = data.get("ts_code")
            list_data = data.get("list")
            if isinstance(list_data, list):
                records = [item for item in list_data if isinstance(item, dict)]

        if records:
            normalized_rows: List[Dict[str, Any]] = []
            for row in records:
                row_ts_code = row.get("ts_code") or row.get("symbol") or row.get("code") or data_ts_code or use_ts_code
                normalized_rows.append({
                    "ts_code": self._to_tushare_ts_code(str(row_ts_code)) if row_ts_code else None,
                    "trade_date": str(row.get("trade_date") or row.get("date") or row.get("day") or "").replace("-", ""),
                    "open": row.get("open", row.get("o")),
                    "high": row.get("high", row.get("h")),
                    "low": row.get("low", row.get("l")),
                    "close": row.get("close", row.get("c")),
                    "pre_close": row.get("pre_close", row.get("prev_close")),
                    "change": row.get("change"),
                    "pct_chg": row.get("pct_chg", row.get("pct_change", row.get("quote_rate"))),
                    "vol": row.get("vol", row.get("volume")),
                    "amount": row.get("amount", row.get("turnover")),
                    "volume": row.get("volume", row.get("vol")),
                    "turnover": row.get("turnover", row.get("amount")),
                    "factor": row.get("factor"),
                    "prev_close": row.get("prev_close", row.get("pre_close")),
                    "avg_price": row.get("avg_price"),
                    "high_limit": row.get("high_limit"),
                    "low_limit": row.get("low_limit"),
                    "turnover_rate": row.get("turnover_rate"),
                    "amp_rate": row.get("amp_rate"),
                    "quote_rate": row.get("quote_rate", row.get("pct_chg", row.get("pct_change"))),
                    "is_paused": row.get("is_paused"),
                    "is_st": row.get("is_st"),
                })
            df = pd.DataFrame(normalized_rows)
        else:
            df = pd.DataFrame()

        export_all = str(kwargs.get("export_all", "")).lower() in ["true", "1", "yes"]
        all_import_columns = [
            "ts_code", "trade_date", "open", "high", "low", "close",
            "volume", "turnover", "factor", "prev_close", "avg_price",
            "high_limit", "low_limit", "turnover_rate", "amp_rate",
            "quote_rate", "is_paused", "is_st"
        ]

        if df.empty:
            if fields == "all" or export_all:
                return pd.DataFrame(columns=all_import_columns)
            else:
                default_columns = [
                    "ts_code", "trade_date", "open", "high", "low", "close",
                    "pre_close", "change", "pct_chg", "vol", "amount"
                ]
                return df.reindex(columns=default_columns)

        if "ts_code" not in df.columns:
            df["ts_code"] = use_ts_code
        else:
            df["ts_code"] = df["ts_code"].apply(lambda x: self._to_tushare_ts_code(str(x)) if pd.notna(x) and str(x) else "")
        if "trade_date" in df.columns:
            df["trade_date"] = df["trade_date"].astype(str).str.replace("-", "", regex=False)
        numeric_columns = [
            "open", "high", "low", "close", "pre_close", "change", "pct_chg", "vol", "amount",
            "volume", "turnover", "factor", "prev_close", "avg_price", "high_limit", "low_limit",
            "turnover_rate", "amp_rate", "quote_rate"
        ]
        for col in numeric_columns:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col], errors="coerce")
        if "change" in df.columns and "pre_close" in df.columns and "close" in df.columns:
            missing_change = df["change"].isna()
            df.loc[missing_change, "change"] = df.loc[missing_change, "close"] - df.loc[missing_change, "pre_close"]
        if "pct_chg" in df.columns and "change" in df.columns and "pre_close" in df.columns:
            missing_pct = df["pct_chg"].isna()
            valid_pre_close = df["pre_close"] != 0
            fill_mask = missing_pct & valid_pre_close
            df.loc[fill_mask, "pct_chg"] = (df.loc[fill_mask, "change"] / df.loc[fill_mask, "pre_close"]) * 100

        if fields == "all" or export_all:
            ordered_columns = all_import_columns
        else:
            ordered_columns = [
                "ts_code", "trade_date", "open", "high", "low", "close",
                "pre_close", "change", "pct_chg", "vol", "amount"
            ]
            if fields:
                requested_fields = [field.strip() for field in fields.split(",") if field.strip()]
                for f in requested_fields:
                    if f in df.columns and f not in ordered_columns:
                        ordered_columns.append(f)

        df = df.reindex(columns=ordered_columns)
        df = df.sort_values(by="trade_date", ascending=False).reset_index(drop=True)
        if use_ts_code:
            if offset is not None:
                df = df.iloc[offset:]
            if limit is not None:
                df = df.head(limit)

        if fields and fields != "all":
            requested_fields = [field.strip() for field in fields.split(",") if field.strip()]
            selected_fields = [field for field in requested_fields if field in df.columns]
            if selected_fields:
                return df[selected_fields]
            return df.iloc[:, 0:0]

        return df

    def stk_mins(
        self,
        ts_code: Optional[str] = None,
        trade_time: Optional[str] = None,
        start_time: Optional[str] = None,
        end_time: Optional[str] = None,
        freq: str = "1min",
        **kwargs: Any
    ):
        use_ts_code = self._to_tushare_ts_code(ts_code) if ts_code else None
        if not use_ts_code:
            raise ValueError("ts_code 不能为空")

        params: Dict[str, Any] = {}
        params["freq"] = freq

        if trade_time:
            params["trade_time"] = trade_time
        if start_time:
            params["start_time"] = start_time
        if end_time:
            params["end_time"] = end_time

        params.update(kwargs)
        url = f"{self.http_url}/v3/market/kline/minute/{use_ts_code}"

        data: Optional[Union[Dict[str, Any], List[Any]]] = None
        try:
            res = requests.get(url, params=params, headers=self.headers, timeout=self.timeout)
            if res.status_code == 200:
                body = res.json()
                if isinstance(body, dict):
                    if body.get("code") == 200:
                        data = body.get("data")
                    elif "data" in body:
                        data = body.get("data")
                    else:
                        data = body
            elif res.status_code == 401:
                logger.error("Unauthorized. Please check your API token at https://quant.zizizaizai.com/me/profile")
            elif res.status_code == 429:
                logger.warning(f"Rate limit exceeded. {res.text}")
            else:
                logger.error(f"HTTP Error: {res.status_code} - {res.text}")
        except Exception as e:
            logger.exception(f"Request Error: {e}")
            data = None

        records: List[Dict[str, Any]] = []
        if isinstance(data, list):
            records = [item for item in data if isinstance(item, dict)]
        elif isinstance(data, dict):
            list_data = data.get("list")
            if isinstance(list_data, list):
                records = [item for item in list_data if isinstance(item, dict)]

        if records:
            normalized_rows: List[Dict[str, Any]] = []
            for row in records:
                row_ts_code = row.get("code") or row.get("ts_code") or use_ts_code
                trade_time_str = row.get("trade_time", "")
                normalized_rows.append({
                    "ts_code": self._to_tushare_ts_code(str(row_ts_code)) if row_ts_code else None,
                    "trade_time": trade_time_str,
                    "open": row.get("open"),
                    "high": row.get("high"),
                    "low": row.get("low"),
                    "close": row.get("close"),
                    "vol": row.get("vol"),
                    "amount": row.get("amount"),
                })
            df = pd.DataFrame(normalized_rows)
        else:
            df = pd.DataFrame()

        if df.empty:
            default_columns = [
                "ts_code", "trade_time", "open", "high", "low", "close", "vol", "amount"
            ]
            return df.reindex(columns=default_columns)

        if "ts_code" not in df.columns:
            df["ts_code"] = use_ts_code
        else:
            df["ts_code"] = df["ts_code"].apply(lambda x: self._to_tushare_ts_code(str(x)) if pd.notna(x) and str(x) else "")

        numeric_columns = ["open", "high", "low", "close", "vol", "amount"]
        for col in numeric_columns:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col], errors="coerce")

        ordered_columns = [
            "ts_code", "trade_time", "open", "high", "low", "close", "vol", "amount"
        ]
        df = df.reindex(columns=ordered_columns)
        df = df.sort_values(by="trade_time", ascending=False).reset_index(drop=True)

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
