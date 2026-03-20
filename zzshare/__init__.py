# -*- coding: utf-8 -*-
from typing import Any, Callable, Optional

from zzshare.client import DataApi


_default_api: Optional[DataApi] = None


def pro_api(token: str = "", timeout: int = 10, http_url: str = "https://api.zizizaizai.com") -> DataApi:
    return DataApi(token=token, timeout=timeout, http_url=http_url)


def _get_default_api() -> DataApi:
    global _default_api
    if _default_api is None:
        _default_api = DataApi()
    return _default_api


def daily(
    code: Optional[str] = None,
    trade_date: Optional[str] = None,
    ts_code: Optional[str] = None,
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    date1: Optional[str] = None,
    date2: Optional[str] = None,
):
    use_code = code or ts_code
    if not use_code:
        raise ValueError("code 或 ts_code 不能为空")
    use_date1 = date1 or trade_date or start_date
    use_date2 = date2 or trade_date or end_date
    return _get_default_api().daily(code=use_code, date1=use_date1, date2=use_date2)


def query(api_name: str, params: Optional[dict] = None):
    return _get_default_api().query(api_name, params=params)


def _create_shortcut_proxy(name: str) -> Callable[..., Any]:
    def _proxy(*args: Any, **kwargs: Any) -> Any:
        return getattr(_get_default_api(), name)(*args, **kwargs)

    _proxy.__name__ = name
    return _proxy


for _shortcut_name in DataApi.SHORTCUTS:
    if _shortcut_name == "daily":
        continue
    globals()[_shortcut_name] = _create_shortcut_proxy(_shortcut_name)


__all__ = ["DataApi", "pro_api", "daily", "query", *[name for name in DataApi.SHORTCUTS if name != "daily"]]
