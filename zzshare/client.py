from functools import partial
import requests
from typing import Any, Optional, Dict, Callable, List, Tuple, Union

from zzshare.core import BaseDataApi
from zzshare.utils import kline_data_to_df


class DataApi(BaseDataApi):
    def __init__(self, token: str = '', timeout: int = 10, http_url: str = 'http://127.0.0.1:9001'):
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
        "market_sentiment_hot_day": (
            "v2/api/sentiment/market/hot/day",
            ["date"],
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
    }

    def _register_shortcuts(self):
        """根据 SHORTCUTS 表动态生成方法"""
        for name, (path_template, param_names, post_process) in self.SHORTCUTS.items():
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
