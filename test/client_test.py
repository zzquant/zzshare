import os
import unittest
from typing import Any, Dict, Optional

from zzshare.client import DataApi


class DataApiTest(unittest.TestCase):
    """
    单元测试基类，支持开关控制是否真实请求
    """

    # 控制是否真实发请求（当前开发状态默认发送）
    REAL_REQUEST = True

    @classmethod
    def setUpClass(cls):
        print(f"\n=== 测试配置：REAL_REQUEST = {cls.REAL_REQUEST} ===\n")

    def setUp(self):
        self.api = DataApi(
            token=os.getenv("API_TOKEN", "fake-token-for-test"),
            timeout=10,
            http_url=os.getenv("API_BASE_URL", "https://api.zizizaizai.com")
        )

    def _call_api_method(self, method_name: str, **kwargs) -> Any:
        """
        统一调用 SDK 方法，并根据开关决定是否真实请求
        """
        method = getattr(self.api, method_name)

        if self.REAL_REQUEST:
            print(f"\n[REAL REQUEST] 调用 {method_name}({kwargs})")

            try:
                result = method(**kwargs)
                print(f"  → 响应类型：{type(result).__name__}")
                print(f"  → 响应：{result}")
                assert result is not None, "响应结果不应为 None"
                return result
            except Exception as e:
                print(f"  → 请求异常：{e}")
                raise

    def test_uplimit_hot(self):
        self._call_api_method("uplimit_hot", date1="2026-02-03")

    def test_uplimit_hot_with_board(self):
        self._call_api_method("uplimit_hot", date1="2026-02-03", board="801070")

    def test_uplimit_stocks(self):
        self._call_api_method("uplimit_stocks", date1="2026-02-03")

    def test_market_plate_stocks_default(self):
        self._call_api_method("market_plate_stocks", plate_code="801070", date1="2026-02-03")

    def test_market_plate_stocks_with_limit(self):
        self._call_api_method("market_plate_stocks", plate_code="801070", date1="2026-02-03", limit=10)

    def test_market_plate_stocks_real_mode(self):
        self._call_api_method("market_plate_stocks", plate_code="801070", date1="2026-02-03", is_real=1)

    def test_market_plate_default(self):
        self._call_api_method("market_plate", date1="2026-02-03")

    def test_market_plate_with_limit(self):
        self._call_api_method("market_plate", date1="2026-02-03", limit=5)

    def test_market_sentiment_single_day(self):
        self._call_api_method("market_sentiment", date1="2026-02-03")

    def test_market_sentiment_range(self):
        self._call_api_method("market_sentiment", date1="2026-02-01", date2="2026-02-03")

    def test_market_hot_sentiment_single_day(self):
        self._call_api_method("market_hot_sentiment", date1="2026-02-03")

    def test_market_hot_sentiment_range(self):
        self._call_api_method("market_hot_sentiment", date1="2026-02-01", date2="2026-02-03")

    def test_ths_hot_top_default(self):
        self._call_api_method("ths_hot_top", date1="2026-02-03")

    def test_ths_hot_top_custom(self):
        self._call_api_method("ths_hot_top", date1="2026-02-03", top_n=50)

    def test_stock_ths_hot(self):
        self._call_api_method("stock_ths_hot", code="600519", date1="2026-02-03")

    def test_market_sentiment_hot_day(self):
        self._call_api_method("sentiment_market_hot_day", date="2026-02-03")

    def test_market_style(self):
        self._call_api_method("market_style", date1="2026-02-03")

    def test_open_sentiment_data_single_day(self):
        self._call_api_method("open_sentiment_data", date1="2026-02-03")

    def test_open_sentiment_data_range(self):
        self._call_api_method("open_sentiment_data", date1="2026-02-01", date2="2026-02-03")

    def test_trade_days_range(self):
        self._call_api_method("trade_days", day_start="2026-02-01", day_end="2026-02-03")

    def test_trade_days_count(self):
        self._call_api_method("trade_days", days=3)

    def test_kline_daily(self):
        self._call_api_method("daily", ts_code="600871.SH", start_date="20260201", end_date="20260203")

    def test_kline_daily_all_by_trade_date(self):
        result = self._call_api_method("daily", trade_date="20260203", limit=5, fields="ts_code,trade_date,open,close")
        assert "ts_code" in result.columns

    def test_sentiment_market_hot_day(self):
        self._call_api_method("sentiment_market_hot_day", date="2026-02-03")

    def test_sentiment_trend_no_date(self):
        self._call_api_method("sentiment_trend", model=0)

    def test_sentiment_trend_with_date(self):
        self._call_api_method("sentiment_trend", model=0, date1="2026-02-03")

    def test_sentiment_trend_range(self):
        self._call_api_method("sentiment_trend_range", model=1, date1="2026-01-01", date2="2026-02-03")

    def test_review_uplimit_reason_default(self):
        self._call_api_method("review_uplimit_reason")

    def test_review_uplimit_reason_custom(self):
        self._call_api_method("review_uplimit_reason", date1="2026-02-03", group=0, page=2, page_size=30)

    def test_review_uplimit_hot_open(self):
        self._call_api_method("review_uplimit_hot_open", date1="2026-02-03")

    def test_stock_uplimit_reason_recent(self):
        self._call_api_method("stock_uplimit_reason", stock_code="600871")

    def test_stock_uplimit_reason_specified_date(self):
        self._call_api_method("stock_uplimit_reason", stock_code="600871", date="2026-02-03")

    def test_stock_uplimit_reason_history_default(self):
        self._call_api_method("stock_uplimit_reason_history", stock_code="000001")

    def test_stock_uplimit_reason_history_page2(self):
        self._call_api_method("stock_uplimit_reason_history", stock_code="000001", page=2, pageSize=20)

    def test_review_uplimit_reason_open_simple(self):
        self._call_api_method("review_uplimit_reason_open", date1="2026-02-03")

    def test_stock_info_basic(self):
        self._call_api_method("stock_info", stock_id="600871", info_type=1)

    def test_stock_basic_default(self):
        result = self._call_api_method("stock_basic")
        assert "ts_code" in result.columns
        assert "symbol" in result.columns
        assert "name" in result.columns

    def test_stock_basic_with_ts_code(self):
        result = self._call_api_method("stock_basic", ts_code="600871.SH")
        assert len(result) > 0
        assert result.iloc[0]["ts_code"] == "600871.SH"

    def test_stock_basic_with_fields(self):
        result = self._call_api_method("stock_basic", ts_code="600871.SH", fields="ts_code,name,exchange")
        assert "ts_code" in result.columns
        assert "name" in result.columns
        assert "exchange" in result.columns
        assert len(result.columns) == 3

    def test_rt_k_single(self):
        result = self._call_api_method("rt_k", ts_code="000001.SZ")
        assert "ts_code" in result.columns
        assert result.iloc[0]["ts_code"] == "000001.SZ"

    def test_rt_k_multiple(self):
        result = self._call_api_method("rt_k", ts_code="000001.SZ,600000.SH")
        assert len(result) >= 2
        assert "000001.SZ" in result["ts_code"].values
        assert "600000.SH" in result["ts_code"].values

    def test_rt_k_wildcard(self):
        # 测试沪市主板通配符
        result = self._call_api_method("rt_k", ts_code="60*.SH")
        assert len(result) > 0
        for code in result["ts_code"]:
            assert code.startswith("60") and code.endswith(".SH")

    def test_rt_k_all_fields(self):
        # 测试全量字段模式
        result = self._call_api_method("rt_k", ts_code="000001.SZ", fields="all")
        assert "high_limit" in result.columns
        assert "turnover_rate" in result.columns
        assert "auction_px" in result.columns


if __name__ == "__main__":
    unittest.main()
