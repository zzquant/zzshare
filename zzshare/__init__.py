# -*- coding: utf-8 -*-
from typing import Any, Callable, Optional

from zzshare.client import DataApi
from zzshare.logger import set_level


_default_api: Optional[DataApi] = None


def pro_api(token: str = "", timeout: int = 10, http_url: str = "https://api.zizizaizai.com") -> DataApi:
    return DataApi(token=token, timeout=timeout, http_url=http_url)


def _get_default_api() -> DataApi:
    global _default_api
    if _default_api is None:
        _default_api = DataApi()
    return _default_api


def daily(
    ts_code: Optional[str] = None,
    trade_date: Optional[str] = None,
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    offset: Optional[int] = None,
    limit: Optional[int] = None,
    fields: Optional[str] = None,
    **kwargs: Any,
):
    return _get_default_api().daily(
        ts_code=ts_code,
        trade_date=trade_date,
        start_date=start_date,
        end_date=end_date,
        offset=offset,
        limit=limit,
        fields=fields,
        **kwargs,
    )


def stock_basic(
    ts_code: Optional[str] = None,
    exchange: Optional[str] = None,
    list_status: str = "L",
    is_hs: Optional[str] = None,
    fields: Optional[str] = None,
    name: Optional[str] = None,
    **kwargs: Any,
):
    return _get_default_api().stock_basic(
        ts_code=ts_code,
        exchange=exchange,
        list_status=list_status,
        is_hs=is_hs,
        fields=fields,
        name=name,
        **kwargs,
    )


def query(api_name: str, params: Optional[dict] = None):
    return _get_default_api().query(api_name, params=params)


def _create_shortcut_proxy(name: str) -> Callable[..., Any]:
    def _proxy(*args: Any, **kwargs: Any) -> Any:
        return getattr(_get_default_api(), name)(*args, **kwargs)

    _proxy.__name__ = name
    return _proxy


for _shortcut_name in DataApi.SHORTCUTS:
    if _shortcut_name in {"daily", "stock_basic"}:
        continue
    globals()[_shortcut_name] = _create_shortcut_proxy(_shortcut_name)


__all__ = ["DataApi", "pro_api", "daily", "stock_basic", "query", "set_level", *[name for name in DataApi.SHORTCUTS if name != "daily"]]
