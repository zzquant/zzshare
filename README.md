# zzshare

`zzshare` 是一个兼容 `tushare pro` 接口规范的 Python 数据包，底层数据对接 `zzzz-market-api`。

---

## 🔥 快捷接口 (SHORTCUTS)

以下为 `DataApi` 类提供的已实现快捷方法，可直接调用：

### 初始化

```python
from zzshare.client import DataApi

api = DataApi()
```

---

### 📊 复盘数据

| 方法名 | 描述 | 参数 |
|:---|:---|:---|
| `uplimit_hot` | 涨停热门板块 | `date1` (日期), `board` (板块, 可选) |
| `uplimit_stocks` | 涨停股票列表 | `date1` (日期) |
| `review_uplimit_reason` | 涨停原因复盘 | `date1`, `group` (分组), `page`, `page_size` |
| `review_uplimit_hot_open` | 涨停热门 (Open) | `date1`, `date2`, `board`, `limit` |
| `review_uplimit_reason_open` | 涨停原因 (Open) | `date1` |

**示例**:
```python
# 获取某日涨停热门板块
data = api.uplimit_hot(date1='20250101')

# 获取某日涨停股票
stocks = api.uplimit_stocks(date1='20250101')
```

---

### 📈 情绪数据

| 方法名 | 描述 | 参数 |
|:---|:---|:---|
| `market_sentiment` | 市场情绪 K 线 (日) | `date1`, `date2` |
| `market_hot_sentiment` | 热门情绪 K 线 (日) | `date1`, `date2` |
| `market_style` | 市场风格择时 | `date1` |
| `open_sentiment_data` | 情绪数据 (Open) | `date1`, `date2` |
| `sentiment_market_hot_day` | 当日市场热度 | `date` |
| `sentiment_trend` | 情绪趋势 | `model` (模型编号), `date1` |
| `sentiment_trend_range` | 情绪趋势区间 | `model`, `date1`, `date2` |

**示例**:
```python
# 获取市场情绪数据
sentiment = api.market_sentiment(date1='20250101', date2='20250131')

# 获取情绪趋势
trend = api.sentiment_trend(model=1, date1='20250101')
```

---

### 🏷️ 板块数据

| 方法名 | 描述 | 参数 |
|:---|:---|:---|
| `market_plate` | 板块排行 | `date1`, `limit` (数量) |
| `market_plate_stocks` | 板块成分股排行 | `plate_code`, `date1`, `is_real`, `limit` |

**示例**:
```python
# 获取板块排行
plates = api.market_plate(date1='20250101', limit=10)

# 获取某板块成分股
stocks = api.market_plate_stocks(plate_code='123456', date1='20250101')
```

---

### 📉 K 线数据

| 方法名 | 描述 | 参数 | 返回 |
|:---|:---|:---|:---|
| `daily` | 日线行情 | `code` (股票代码), `date1`, `date2` | `DataFrame` |

**示例**:
```python
# 获取某只股票日线数据
df = api.daily(code='000001', date1='20250101', date2='20250131')
print(df)
```

---

### 📅 基础数据

| 方法名 | 描述 | 参数 |
|:---|:---|:---|
| `trade_days` | 交易日历表 | `day_start`, `day_end`, `days` |

**示例**:
```python
# 获取最近 30 个交易日
days = api.trade_days(days=30)
```

---

### 🔥 第三方热度数据

| 方法名 | 描述 | 参数 |
|:---|:---|:---|
| `ths_hot_top` | 同花顺热度排行 | `date1`, `top_n` (数量) |
| `stock_ths_hot` | 个股同花顺热度 | `code` (股票代码), `date1` |

**示例**:
```python
# 获取同花顺热度 Top 100
hot_top = api.ths_hot_top(date1='20250101', top_n=100)

# 获取某只股票的同花顺热度
stock_hot = api.stock_ths_hot(code='000001', date1='20250101')
```

---

### 📌 个股数据

| 方法名 | 描述 | 参数 |
|:---|:---|:---|
| `stock_uplimit_reason` | 个股涨停原因 | `stock_code`, `date` |
| `stock_uplimit_reason_history` | 个股涨停历史 | `stock_code`, `page`, `pageSize` |
| `stock_info` | 个股信息 | `stock_id`, `info_type` |
| `stock_moneyflow` | 个股资金流向 | `stock_id`, `m_type` |

**示例**:
```python
# 获取某只股票涨停原因
reason = api.stock_uplimit_reason(stock_code='000001', date='20250101')

# 获取某只股票涨停历史
history = api.stock_uplimit_reason_history(stock_code='000001', page=1, pageSize=10)

# 获取个股信息
info = api.stock_info(stock_id='000001', info_type=1)
```

---

### 🐉 龙虎榜数据

| 方法名 | 描述 | 参数 |
|:---|:---|:---|
| `lhb_list` | 龙虎榜列表 | `date1` |
| `lhb_detail` | 龙虎榜详情 | `date1`, `stock_code` |
| `lhb_stock_history` | 个股龙虎榜历史 | `stock_code`, `trader_name` (可选) |
| `lhb_trader_history` | 席位交易历史 | `trader_name`, `trader_id`, `stock_code`, `page`, `per_page` |

**示例**:
```python
# 获取某日龙虎榜
lhb = api.lhb_list(date1='20250101')

# 获取龙虎榜详情
detail = api.lhb_detail(date1='20250101', stock_code='000001')

# 获取某只股票龙虎榜历史
history = api.lhb_stock_history(stock_code='000001')
```

---

### 🏷️ 板块扩展数据

| 方法名 | 描述 | 参数 |
|:---|:---|:---|
| `plates_list` | 板块列表 | `plate_type` |
| `plates_rank` | 板块排名 | `plate_type`, `date1`, `limit` |
| `plates_trend` | 板块趋势 | `plate_type`, `plate_code`, `day_start`, `day_end` |
| `plates_stocks` | 板块成分股 | `plate_type`, `plate_code`, `date` |

**示例**:
```python
# 获取板块列表 (7=精选, 5=概念, 4=行业)
plates = api.plates_list(plate_type=7)

# 获取板块排名
rank = api.plates_rank(plate_type=7, date1='20250101', limit=20)

# 获取板块趋势
trend = api.plates_trend(plate_type=7, plate_code='123456', day_start='20250101', day_end='20250131')
```

---

### 📊 涨跌分布与情绪

| 方法名 | 描述 | 参数 |
|:---|:---|:---|
| `updown_distribution` | 涨跌分布 | `date1` |
| `uplimit_trend` | 涨停趋势 | `date1` |
| `sentiment_hot_day` | 日度市场热度 | `index`, `st` |
| `sentiment_level` | 情绪级别 | `date` |
| `sentiment_bull_data` | 牛熊情绪数据 | `date1`, `date2` |

**示例**:
```python
# 获取涨跌分布
dist = api.updown_distribution(date1='20250101')

# 获取涨停趋势
trend = api.uplimit_trend(date1='20250101')

# 获取情绪级别
level = api.sentiment_level(date='20250101')
```

---

### 📈 行情实时数据

| 方法名 | 描述 | 参数 |
|:---|:---|:---|
| `market_real` | 行情实时快照 | `symbols` (逗号分隔) |
| `market_mf` | 资金流向分钟 | `stock`, `date`, `wm`, `default_v` |

**示例**:
```python
# 获取多只股票实时行情
real = api.market_real(symbols='000001,000002,000003')

# 获取资金流向分钟数据
mf = api.market_mf(stock='000001', date='2025-01-01 0930')
```

---

### 📉 涨停市值与异动

| 方法名 | 描述 | 参数 |
|:---|:---|:---|
| `uplimit_market_value` | 涨停市值统计 | `date1`, `date2` |
| `sentiment_market_top_n` | 市场 TopN 情绪 | `modal_id`, `date1`, `date2` |
| `movement_alerts` | 异动数据 | `date1`, `type`, `limit`, `is_real` |
| `zdjk_get` | 监控数据 | `date1`, `date2` |

**示例**:
```python
# 获取涨停市值统计
mv = api.uplimit_market_value(date1='20250101', date2='20250131')

# 获取异动数据
alerts = api.movement_alerts(date1='20250101', limit=100)
```

---

### 🔧 通用查询

除了以上快捷方法，还可以使用通用 `query` 方法自定义调用任意 API：

```python
# 通用查询
result = api.query('your/custom/path', params={'key': 'value'})
```

---

## 📦 安装

```bash
# 进入项目目录
pip install -e .
```

## 🚀 快速开始

```python
import zzshare as zz

# 初始化接口 (token 可选)
pro = zz.pro_api()

# 1. 获取日线行情 (✅ 已对接)
df = pro.daily(symbol_code='000001.SZ', start_date='20241201', end_date='20241230')
print(df)

# 2. 获取涨停板数据 (✅ 已对接)
df_limit = pro.limit_list(trade_date='20241226')
print(df_limit)
```

## 📚 接口列表

符号说明：
- ✅ **已实现**：对接真实数据
- 🚧 **TODO**：接口已定义，暂返回空数据 (等待后端支持)

### 1. 基础数据 (Base Data)

| 接口名称 | 描述 | 状态 |
| :--- | :--- | :--- |
| `stock_basic` | 股票列表 | 🚧 |
| `trade_cal` | 交易日历 | 🚧 |
| `stock_company` | 上市公司基本信息 | 🚧 |
| `stk_managers` | 上市公司管理层 | 🚧 |
| `stk_rewards` | 管理层薪酬 | 🚧 |
| `new_share` | IPO新股列表 | 🚧 |
| `hs_const` | 沪深股通成份股 | 🚧 |
| `namechange` | 股票曾用名 | 🚧 |

### 2. 行情数据 (Market Data)

| 接口名称 | 描述 | 状态 |
| :--- | :--- | :--- |
| `daily` | **日线行情** | ✅ |
| `limit_list` | **每日涨停统计** | ✅ |
| `moneyflow_hsgt` | 沪深港通资金流向 | 🚧 |
| `moneyflow` | 个股资金流向 | 🚧 |
| `stk_mins` | 分钟行情 | 🚧 |



### 3. 财务数据 (Financial Data)

| 接口名称 | 描述 | 状态 |
| :--- | :--- | :--- |
| `income` | 利润表 | 🚧 |
| `balancesheet` | 资产负债表 | 🚧 |
| `cashflow` | 现金流量表 | 🚧 |
| `forecast` | 业绩预告 | 🚧 |
| `express` | 业绩快报 | 🚧 |
| `dividend` | 分红送转 | 🚧 |
| `fina_indicator` | 财务指标数据 | 🚧 |
| `fina_audit` | 财务审计意见 | 🚧 |
| `fina_mainbz` | 主营业务构成 | 🚧 |
| `disclosure_date` | 财报披露计划 | 🚧 |

### 4. 市场参考 (Market Reference)

| 接口名称 | 描述 | 状态 |
| :--- | :--- | :--- |
| `margin` | 融资融券交易汇总 | 🚧 |
| `margin_detail` | 融资融券交易明细 | 🚧 |
| `top10_holders` | 前十大股东 | 🚧 |
| `top10_floatholders` | 前十大流通股东 | 🚧 |
| `top_list` | 龙虎榜 | 🚧 |
| `block_trade` | 大宗交易 | 🚧 |
| `stk_holdertrade` | 董监高持股变动 | 🚧 |
| `pledge_stat` | 股权质押统计 | 🚧 |
| `pledge_detail` | 股权质押明细 | 🚧 |
| `repurchase` | 股票回购 | 🚧 |
| `concept` | 概念股分类 | 🚧 |
| `concept_detail` | 概念股列表 | 🚧 |

### 5. 指数数据 (Index Data)

| 接口名称 | 描述 | 状态 |
| :--- | :--- | :--- |
| `index_basic` | 指数基本信息 | 🚧 |
| `index_daily` | 指数日线行情 | 🚧 |
| `index_weight` | 指数成分和权重 | 🚧 |
| `index_dailybasic` | 指数每日指标 | 🚧 |
| `index_classify` | 申万行业分类 | 🚧 |
| `index_member` | 申万行业成分 | 🚧 |

### 6. 基金数据 (Fund Data)

| 接口名称 | 描述 | 状态 |
| :--- | :--- | :--- |
| `fund_basic` | 公募基金列表 | 🚧 |
| `fund_net_value` | 公募基金净值 | 🚧 |
| `fund_daily` | 场内基金日线行情 | 🚧 |

### 7. 新闻/事件 (News & Events)

| 接口名称 | 描述 | 状态 |
| :--- | :--- | :--- |
| `news` | 新闻资讯 | 🚧 |
| `major_news` | 大事提醒 | 🚧 |
| `cctv_news` | 新闻联播 | 🚧 |

### 8. 衍生品与海外 (Derivatives & Global)

| 接口名称 | 描述 | 状态 |
| :--- | :--- | :--- |
| `cb_basic` | 可转债基础信息 | 🚧 |
| `cb_daily` | 可转债行情 | 🚧 |
| `fut_daily` | 期货日线行情 | 🚧 |
| `opt_daily` | 期权日线行情 | 🚧 |
| `us_daily` | 美股日线行情 | 🚧 |
| `hk_basic` | 港股列表 | 🚧 |

### 9. 宏观与利率 (Macro & Interest)

| 接口名称 | 描述 | 状态 |
| :--- | :--- | :--- |
| `shibor` | Shibor利率 | 🚧 |
| `libor` | Libor利率 | 🚧 |
| `hibor` | Hibor利率 | 🚧 |
| `cn_gdp` | 中国GDP | 🚧 |
| `cn_cpi` | 中国CPI | 🚧 |
| `cn_ppi` | 中国PPI | 🚧 |
| `cn_m` | 中国货币供应量 | 🚧 |
| `us_tycr` | 美国国债收益率 | 🚧 |

### 10. 基金扩展 (Fund Extended)

| 接口名称 | 描述 | 状态 |
| :--- | :--- | :--- |
| `fund_manager` | 基金经理 | 🚧 |
| `fund_share` | 基金份额 | 🚧 |
| `fund_nav` | 基金净值(Open) | 🚧 |
| `fund_portfolio` | 基金持仓 | 🚧 |

### 11. 债券 (Bond)

| 接口名称 | 描述 | 状态 |
| :--- | :--- | :--- |
| `bond_basic` | 债券列表 | 🚧 |
| `bond_issue` | 债券发行 | 🚧 |
| `bond_daily` | 债券行情 | 🚧 |
| `bond_blk` | 债券大宗交易 | 🚧 |

### 12. 股票特色 (Stock Feature)

| 接口名称 | 描述 | 状态 |
| :--- | :--- | :--- |
| `stk_surv` | 机构调研 | 🚧 |
| `broker_recommend` | 券商推荐 | 🚧 |
| `hk_hold` | 沪深港股通持股 | 🚧 |
| `stk_limit` | 每日涨跌停价格 | 🚧 |
| `daily_basic` | 每日指标 | 🚧 |
| `bak_daily` | 备用行情 | 🚧 |
| `bak_basic` | 备用基础信息 | 🚧 |

### 13. 其他扩展 (Others)

| 接口名称 | 描述 | 状态 |
| :--- | :--- | :--- |
| `index_global` | 国际指数 | 🚧 |
| `index_weekly` | 指数周线 | 🚧 |
| `index_monthly` | 指数月线 | 🚧 |
| `fut_weekly` | 期货周线 | 🚧 |
| `fut_monthly` | 期货月线 | 🚧 |

### 14. 财务/行情扩展 (Financial & Market Extended)

| 接口名称 | 描述 | 状态 |
| :--- | :--- | :--- |
| `weekly` | 周线行情 | 🚧 |
| `monthly` | 月线行情 | 🚧 |
| `adj_factor` | 复权因子 | 🚧 |
| `suspend_d` | 停复牌信息 | 🚧 |
| `hsgt_top10` | 沪深股通十大成交股 | 🚧 |
| `ggt_top10` | 港股通十大成交股 | 🚧 |
| `ggt_daily` | 港股通日线行情 | 🚧 |

## ⚙️ 配置说明

可在 `zzshare.client.DataApi` 中通过构造函数传入自定义配置。
