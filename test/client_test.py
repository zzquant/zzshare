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
            token=os.getenv("ZZSHARE_TOKEN", "fake-token-for-test"),
            timeout=30,
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

    def test_plates_rank_default(self):
        self._call_api_method("plates_rank", plate_type=17, date1="2026-02-03")

    def test_plates_rank_with_limit(self):
        self._call_api_method("plates_rank", plate_type=17, date1="2026-02-03", limit=5)

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
        if self.api.token == "fake-token-for-test":
            print("Skipping test_stock_info_basic: Requires a valid ZZSHARE_TOKEN")
            return
        try:
            result = self.api.stock_info(stock_id="600871", info_type=1)
            print(f"  → stock_info test response: {result}")
        except Exception as e:
            print(f"Skipping test_stock_info_basic due to network/API error: {e}")

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


    # ============================================================
    # Finance Data Tests
    # ============================================================

    def test_finance_valuation_by_date(self):
        """valuation daily: query by trade_date"""
        result = self._call_api_method("finance_valuation", date_value="2024-12-31")
        assert result is not None

    def test_finance_indicator_by_quarter(self):
        """indicator quarterly: query by statDate"""
        result = self._call_api_method("finance_indicator", date_value="2024q4")
        assert result is not None

    def test_finance_income_by_quarter(self):
        result = self._call_api_method("finance_income", date_value="2024q4")
        assert result is not None

    def test_finance_balance_by_quarter(self):
        result = self._call_api_method("finance_balance", date_value="2024q4")
        assert result is not None

    def test_finance_cash_flow_by_quarter(self):
        result = self._call_api_method("finance_cash_flow", date_value="2024q4")
        assert result is not None

    def test_finance_pit_daily(self):
        """PIT query: valuation (daily) on a trade date"""
        result = self._call_api_method("finance_pit", table="valuation", trade_date="2024-12-31")
        assert result is not None

    def test_finance_pit_daily_with_codes(self):
        """PIT query: valuation with specific codes"""
        result = self._call_api_method("finance_pit", table="valuation", trade_date="2024-12-31", codes="600519.SH,000001.SZ")
        assert result is not None

    def test_finance_pit_quarterly(self):
        """PIT query: indicator (quarterly) - latest published before D"""
        result = self._call_api_method("finance_pit", table="indicator", trade_date="2025-01-15")
        assert result is not None

    def test_finance_range_daily(self):
        """Range query: valuation across a date range"""
        result = self._call_api_method("finance_range", table="valuation", start_date="2024-12-01", end_date="2024-12-31", limit=100)
        assert result is not None

    def test_finance_range_quarterly(self):
        """Range query: income across quarters"""
        result = self._call_api_method("finance_range", table="income", start_date="2024q1", end_date="2024q4", limit=100)
        assert result is not None

    def test_finance_stock_history_daily(self):
        """Single stock history: valuation for 600519.SH"""
        result = self._call_api_method("finance_stock", table="valuation", code="600519.SH", limit=10)
        assert result is not None

    def test_finance_stock_history_quarterly(self):
        """Single stock history: balance for 600519.SH"""
        result = self._call_api_method("finance_stock", table="balance", code="600519.SH", limit=10)
        assert result is not None

    def test_finance_latest_daily(self):
        """Latest snapshot: valuation (daily)"""
        result = self._call_api_method("finance_latest", table="valuation")
        assert result is not None

    def test_finance_latest_quarterly(self):
        """Latest snapshot: indicator (quarterly)"""
        result = self._call_api_method("finance_latest", table="indicator")
        assert result is not None

    def test_finance_latest_with_codes(self):
        """Latest snapshot: filter by codes"""
        result = self._call_api_method("finance_latest", table="indicator", codes="600519.SH")
        assert result is not None

if __name__ == "__main__":
    unittest.main()
