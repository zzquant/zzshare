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
        self._call_api_method("market_sentiment_hot_day", date="2026-02-03")

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
        self._call_api_method("daily", code="600871", date1="2026-02-01", date2="2026-02-03")


if __name__ == "__main__":
    unittest.main()
