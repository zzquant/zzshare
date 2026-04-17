<p align="center">
  <h1 align="center">📈 zzshare</h1>
  <p align="center">
    <strong>A股量化数据接口 · 免费 · 开箱即用</strong>
  </p>
  <p align="center">
    <a href="#-快速开始">快速开始</a> •
    <a href="#-接口一览">接口一览</a> •
    <a href="#-使用示例">使用示例</a> •
    <a href="#-常见问题">FAQ</a>
  </p>
</p>

***

## ✨ 特性

- 🚀 **开箱即用** - 无需申请，安装即可使用
- 📅 **数据范围** - 行情数据2005年至今(20年+)，其他数据根据接口提供方数据为准。
- 📊 **丰富数据** - 行情数据、涨停复盘、龙虎榜、情绪指标、板块热度等 40+ 接口。
- 🔄 **兼容 某些接口** - 接口规范兼容某些接口,比如tushare等。
- ⚡ **实时数据** - 支持日线、分钟线、资金流向等盘中实时数据。
- 🐍 **类型提示** - 完整的 `.pyi` 类型文件，IDE 自动补全。

***

## 📦 安装

**推荐安装方式（通过 PyPI）**：

```bash
# 基础安装
pip install zzshare
```

<details>
<summary><b>高级安装选项</b></summary>

如果你想体验最新的开发版本（可能包含未发布的特性）：

```bash
pip install git+https://github.com/zzquant/zzshare.git
```

或克隆后本地安装：

```bash
git clone https://github.com/zzquant/zzshare.git
cd zzshare
pip install -e .
```

</details>

## 更新

```bash
pip install zzshare --upgrade
```

***

## 🚀 快速开始

**使用 API Token 初始化：**

```python
from zzshare.client import DataApi

# [可选,提高访问频率使用]Token 可在官网个人资料页面获取(https://quant.zizizaizai.com/me/profile)
api = DataApi(token='your_api_token_here')

# 获取日线行情
df = api.daily(ts_code='000001.SZ', start_date='20260302', end_date='20260331')
print(df)
```

**更多示例：**

```python
# 查询全市场股票列表（SS/KSH/SZ/GEM/BJ）
stock_list = api.stock_basic(exchange='',fields='ts_code,name,exchang')



# 获取今日涨停热门板块
hot = api.uplimit_hot(date1='20250205')

# 获取龙虎榜
lhb = api.lhb_list(date1='20250205')

# 获取同花顺热度 Top 100
ths_top = api.ths_hot_top(date1='20250205', top_n=100)

# 获取交易日历
days = api.trade_days(days=30)

# tushare 兼容：获取股票列表
basic = api.stock_basic(exchange='SSE', list_status='L', fields='ts_code,symbol,name,exchange,list_status')
```

***

## 📊 接口一览

### 核心接口 (已实现)

| 分类 | 核心接口 | 功能描述 |
| :--- | :--- | :--- |
| **基础行情** | `daily`, `stk_mins`, `rt_k` | 历史日K、分钟K、实时快照（支持复权） |
| **基础数据** | `stock_basic`, `trade_days`, `stock_info` | 股票列表、交易日历、个股基础资料 |
| **涨停复盘** | `uplimit_hot`, `uplimit_stocks`, `stock_uplimit_reason` | 涨停梯队、热门板块、个股涨停原因 |
| **龙虎榜单** | `lhb_list`, `lhb_detail`, `lhb_stock_history` | 龙虎榜列表、个股详情、席位交易历史 |
| **情绪热度** | `market_sentiment`, `sentiment_trend`, `ths_hot_top` | 市场情绪指标、情绪趋势、同花顺热度 |
| **板块分析** | `plates_list`, `plates_rank`, `market_plate` | 行业/概念板块列表、排名、热门成分股 |
| **资金流向** | `stock_moneyflow`, `market_mf` | 个股实时资金流向、市场分钟级资金监控 |

> 💡 共计 **40+** 个已实现接口，完整列表见下方。

***

## 📖 使用示例

### 股票基础信息（兼容）

```python
# 获取上交所在市股票（默认 list_status='L'）
df_sse = api.stock_basic(
    exchange='SSE',
    list_status='L',
    fields='ts_code,symbol,name,exchange,list_status'
)

# exchange 为空时默认查询全市场（SS/KSH/SZ/GEM/BJ）
df_all_default = api.stock_basic(
    exchange='',
    list_status='L',
    fields='ts_code,symbol,name,exchange,list_status'
)

# 获取科创板股票（扩展市场）
df_ksh = api.stock_basic(
    exchange='KSH',
    fields='ts_code,symbol,name,market,exchange'
)

# 获取全市场（含主板/科创板/创业板/北交所）
df_all = api.stock_basic(
    exchange='ALL',
    list_status='L',
    fields='ts_code,symbol,name,market,exchange,list_status'
)

```

`stock_basic` 的 `exchange` 支持以下取值（大小写不敏感）：

- `SSE` 或 `SH` 或 `SS`：上海证券交易所（主板）
- `KSH` 或 `STAR`：上海科创板
- `SZSE` 或 `SZ`：深圳证券交易所（主板）
- `BSE` 或 `BJ`：北京证券交易所
- `GEM`：创业板（当前后端按独立市场维度提供）
- `ALL`：全市场（SS/KSH/SZ/GEM/BJ）

`stock_basic` 的 `list_status` 支持：

- `L`：上市
- `D`：退市
- `P`：上市暂停（当前返回空表，但保留 tushare 兼容字段）

### 历史日线行情（兼容）

- 数据说明：交易日收盘后提供(沪深京)
- 全量字段中有复权因子,方便量化用户导出数据。
- 数据起始2005年

```python
# 获取单只股票的日线数据（指定日期范围）
df = api.daily(
    ts_code='600871.SH',
    start_date='20260201',
    end_date='20260203'
)

# 获取单只股票的日线数据（指定单个交易日）
df = api.daily(
    ts_code='600871.SH',
    trade_date='20260203'
)

# 获取全市场某交易日的所有股票数据（分页）
df = api.daily(
    trade_date='20260203',
    offset=0,
    limit=10
)

# 指定返回字段
df = api.daily(
    ts_code='600871.SH',
    start_date='20260201',
    end_date='20260203',
    fields='ts_code,trade_date,open,high,low,close,pct_chg,vol,amount'
)

# 使用复权参数（adj='qfq' 前复权，adj='hfq' 后复权）
df = api.daily(
    ts_code='600871.SH',
    start_date='20260101',
    end_date='20260203',
    adj='qfq'
)
# 获取全市场某交易日的所有股票数据（分页）
df = api.daily(trade_date='20260331',offset=0, limit=10)

```

`daily` 接口返回的字段说明：

| 字段名 | 说明 |
| :--- | :--- |
| `ts_code` | 股票代码（格式：600871.SH） |
| `trade_date` | 交易日期（格式：20260203） |
| `open` | 开盘价 |
| `high` | 最高价 |
| `low` | 最低价 |
| `close` | 收盘价 |
| `pre_close` | 昨收价 |
| `change` | 涨跌额 |
| `pct_chg` | 涨跌幅（%） |
| `vol` | 成交量（股） |
| `amount` | 成交额（元） |

`daily` 接口参数说明：

- `ts_code`：股票代码，格式如 `600871.SH` 或 `000001.SZ`。为空时查询全市场数据
- `trade_date`：交易日期，格式如 `20260203`。当 `ts_code` 为空时必填
- `start_date`：起始日期，格式如 `20260201`
- `end_date`：结束日期，格式如 `20260203`
- `offset`：偏移量，用于分页
- `limit`：返回记录数，用于分页
- `fields`：指定返回字段，如 `ts_code,trade_date,close,pct_chg`。传入 `'all'` 可返回以下所述的原始底层全量字段
- `adj`：复权类型，`qfq` 前复权，`hfq` 后复权，默认不复权
- `export_all`：设为 `True` 时直接返回更多的 18 个全量字段模式

> ✨ **全量字段模式说明**：
>
> 为了最大化兼容，默认仅返回上表的 11 种核心字段。
> 但如果您传入 `fields='all'` 或 `export_all=True` 参数，接口将返回 **全部 18 个字段**，以供高阶量化计算所需（需要注意：全量模式下底层原生的 `volume`/`turnover`/`quote_rate` 名字会直接替代缩写版的 `vol`/`amount`/`pct_chg`）。全量模式补充的特殊字段如下：
>
> - `factor`：复权因子
> - `avg_price`：日内均价
> - `high_limit` / `low_limit`：涨停价 / 跌停价
> - `turnover_rate`：换手率
> - `amp_rate`：振幅
> - `is_paused` / `is_st`：是否停牌 / 是否 ST

### 实时日线（兼容）

- 数据说明：实时获取 A 股快照数据，支持单支、多代码并发以及通配符筛选全市场。
- **注意**：本接口需要token才能使用, 限制20次/分钟,token在官网个人资料页面获取(<https://quant.zizizaizai.com/me/profile>)

```python
# 获取单只股票的实时快照
df = api.rt_k(ts_code='600000.SH')

# 并发获取多只股票的实时快照（使用逗号分隔）
df = api.rt_k(ts_code='600000.SH,000001.SZ')


# 支持通配符：一次性过滤获取所有沪市实时快照
df = api.rt_k(ts_code='60*.SH,68*.SH')
# 支持通配符：一次性过滤获取所有沪市主板实时快照
df = api.rt_k(ts_code='60*.SH')
# 支持通配符：一次性过滤获取所有科创板实时快照
df = api.rt_k(ts_code='68*.SH')

# 支持通配符：一次性过滤获取所有深市实时快照
df = api.rt_k(ts_code='0*.SZ,3*.SZ')
# 支持通配符：一次性过滤获取所有深市主板实时快照
df = api.rt_k(ts_code='0*.SZ')
# 支持通配符：一次性过滤获取所有创业板实时快照
df = api.rt_k(ts_code='3*.SZ')

# 支持通配符：一次性过滤获取所有北交所实时快照
df = api.rt_k(ts_code='9*.BJ')

#支持通配符：获取今日开盘以来全市场所有股票实时日线（不建议一次提取全市场，分批提取更快）
df = api.rt_k(ts_code='3*.SZ,0*.SZ,6*.SH,9*.BJ')

# 获取底层全量字段视图（如换手率、涨跌幅、总市值、涨跌停价、竞价成交价、竞价成交量、竞价成交额、多档买盘数据、多档卖盘数据、滚动市盈率、滚动每股收益 等高级指标）
df = api.rt_k(ts_code='000001.SZ', fields='all')
```

`rt_k` 接口默认返回的底层兼容 14 字段说明：

| 字段名 | 说明 |
| :--- | :--- |
| `ts_code` | 股票代码 |
| `name` | 股票名称 |
| `pre_close` | 昨收价 |
| `high` | 最高价 |
| `open` | 开盘价 |
| `low` | 最低价 |
| `close` | 现价/实时收盘价 |
| `vol` | 成交量（股） |
| `amount` | 成交金额（元） |
| `num` | 成交笔数（若源不支持则返回 0） |
| `ask_price1` | 卖一价 |
| `ask_volume1` | 卖一量 |
| `bid_price1` | 买一价 |
| `bid_volume1` | 买一量 |

> 🚀 **增强模式说明**：
> 当指定了 `fields='all'`，接口将会在此基础上补充透传以下高级量化数据（收到数据后，内置会自动将其转为 `float/int` 类型）：
>
> - **行情涨势**：`quote_rate`（涨跌幅）、`turnover_rate`（换手率）、`min5_chgpct`（5分钟涨跌幅）
> - **市值与限额**：`high_limit` / `low_limit`（涨跌停价）、`market_value` / `circulation_value`（总市值 / 流通市值）
> - **集合竞价**：`auction_px`（竞价成交价）、`auction_vol`（竞价成交量）、`auction_val`（竞价成交额）
> - **切片盘口**：`bid_grp`（多档买盘数据）、`offer_grp`（多档卖盘数据）
> - **财务估值**：`ttm_pe_rate`（滚动市盈率）、`eps_ttm`（滚动每股收益）

### 分钟K线（兼容）

```python
# 获取某日1分钟K线
df = api.stk_mins(
    ts_code='000001',
    trade_time='20250403',
    freq='1min'
)

# 获取某日5分钟K线
df = api.stk_mins(
    ts_code='600000.SH',
    trade_time='20250403',
    freq='5min'
)

# 按时间区间查询
df = api.stk_mins(
    ts_code='000001',
    start_time='20250403 09:30:00',
    end_time='20250403 10:00:00',
    freq='1min'
)

# 指定时间点查询（从该时间点开始获取）
df = api.stk_mins(
    ts_code='000001',
    trade_time='20250403 14:30:00',
    freq='1min'
)
```

`stk_mins` 接口返回的字段说明：

| 字段名 | 说明 |
| :--- | :--- |
| `ts_code` | 股票代码（格式：600871.SH） |
| `trade_time` | 交易时间（格式：202504031430） |
| `open` | 开盘价 |
| `high` | 最高价 |
| `low` | 最低价 |
| `close` | 收盘价 |
| `vol` | 成交量（股） |
| `amount` | 成交额（元） |

- **注意**：本接口在未配置 Token 的情况下，访问频率（30次/分钟）。如需更高频次调用，请配置您的 SDK Token。

`stk_mins` 接口参数说明：

- `ts_code`：股票代码，格式如 `600871.SH` 或 `000001.SZ`（必填）
- `freq`：行情频率，支持 `1min`/`5min`/`15min`/`30min`/`60min`，默认 `1min`
- `trade_time`：交易时间，格式如 `20250403` 或 `20250403 14:30:00`
- `start_time`：开始时间，格式如 `20250403 09:30:00`
- `end_time`：结束时间，格式如 `20250403 15:00:00`

**查询方式说明**：

1. **按单日查询**：传入 `trade_time='20250403'`，返回该日全天数据
2. **按时间区间查询**：传入 `start_time` 和 `end_time`，返回区间内数据
3. **按时间点查询**：传入 `trade_time='20250403 14:30:00'`，从该时间点开始获取

### 涨停复盘

```python
# 获取某日涨停热门板块
hot = api.uplimit_hot(date1='20250205')

# 获取某日涨停股票列表
stocks = api.uplimit_stocks(date1='20250205')

# 获取个股涨停原因
reason = api.stock_uplimit_reason(stock_code='000001', date='20250205')
```

### 龙虎榜

```python
# 获取龙虎榜列表
lhb = api.lhb_list(date1='20250205')

# 获取龙虎榜详情
detail = api.lhb_detail(date1='20250205', stock_code='000001')

# 获取个股龙虎榜历史
history = api.lhb_stock_history(stock_code='000001')
```

### 板块数据

```python
# 获取板块列表 (7=精选, 5=概念, 4=行业)
plates = api.plates_list(plate_type=7)

# 获取板块排名
rank = api.plates_rank(plate_type=7, date1='20250205', limit=20)

# 获取板块成分股
stocks = api.market_plate_stocks(plate_code='123456', date1='20250205')
```

### 情绪指标

```python
# 获取市场情绪K线
sentiment = api.market_sentiment(date1='20250101', date2='20250205')

# 获取情绪趋势
trend = api.sentiment_trend(model=1, date1='20250205')

# 获取情绪级别
level = api.sentiment_level(date='20250205')
```

***

## 📚 完整接口列表

<details>
<summary><b>点击展开全部接口</b></summary>

### 基础数据

| 方法名           | 描述                          | 参数                                                              |
| :------------ | :-------------------------- | :-------------------------------------------------------------- |
| `trade_days`  | 交易日历                        | `day_start`, `day_end`, `days`                                  |
| `stock_basic` | 股票基础信息,各个市场股票列表（tushare 兼容） | `ts_code`, `exchange`, `list_status(L/D/P)`, `is_hs`, `fields`, `name` |

`stock_basic.exchange` 说明：

- `SSE/SH/SS` = 上交所
- `KSH/STAR` = 科创板
- `SZSE/SZ` = 深交所
- `BSE/BJ` = 北交所
- `GEM` = 创业板
- `ALL` = 全市场（SS/KSH/SZ/GEM/BJ）

### 复盘数据

| 方法名                          | 描述     | 参数                                    |
| :--------------------------- | :----- | :------------------------------------ |
| `uplimit_hot`                | 涨停热门板块 | `date1`, `board`                      |
| `uplimit_stocks`             | 涨停股票列表 | `date1`                               |
| `review_uplimit_reason`      | 涨停原因复盘 | `date1`, `group`, `page`, `page_size` |
| `review_uplimit_hot_open`    | 涨停热门   | `date1`, `date2`, `board`, `limit`    |
| `review_uplimit_reason_open` | 涨停原因   | `date1`                               |

### 情绪数据

| 方法名                        | 描述     | 参数                        |
| :------------------------- | :----- | :------------------------ |
| `market_sentiment`         | 市场情绪K线 | `date1`, `date2`          |
| `market_hot_sentiment`     | 热门情绪K线 | `date1`, `date2`          |
| `market_style`             | 市场风格择时 | `date1`                   |
| `open_sentiment_data`      | 情绪数据   | `date1`, `date2`          |
| `sentiment_market_hot_day` | 当日市场热度 | `date`                    |
| `sentiment_trend`          | 情绪趋势   | `model`, `date1`          |
| `sentiment_trend_range`    | 情绪趋势区间 | `model`, `date1`, `date2` |
| `updown_distribution`      | 涨跌分布   | `date1`                   |
| `uplimit_trend`            | 涨停趋势   | `date1`                   |
| `sentiment_hot_day`        | 日度市场热度 | `index`, `st`             |
| `sentiment_level`          | 情绪级别   | `date`                    |
| `sentiment_bull_data`      | 牛熊情绪   | `date1`, `date2`          |

### 板块数据

| 方法名                   | 描述      | 参数                                                 |
| :-------------------- | :------ | :------------------------------------------------- |
| `market_plate`        | 板块排行    | `date1`, `limit`                                   |
| `market_plate_stocks` | 板块成分股排行 | `plate_code`, `date1`, `is_real`, `limit`          |
| `plates_list`         | 板块列表    | `plate_type`                                       |
| `plates_rank`         | 板块排名    | `plate_type`, `date1`, `limit`                     |
| `plates_trend`        | 板块趋势    | `plate_type`, `plate_code`, `day_start`, `day_end` |
| `plates_stocks`       | 板块成分股   | `plate_type`, `plate_code`, `date`                 |

### K线数据

| 方法名       | 描述                     | 参数                                                                                              | 返回        |
| :-------- | :--------------------- | :---------------------------------------------------------------------------------------- | :-------- |
| `daily`   | 日线行情（tushare 兼容）   | `ts_code`, `trade_date`, `start_date`, `end_date`, `offset`, `limit`, `fields`, `adj`                          | DataFrame |
| `stk_mins` | 分钟K线（tushare 兼容） | `ts_code`, `freq`, `trade_time`, `start_time`, `end_time`                                                | DataFrame |

### 热度数据

| 方法名             | 描述      | 参数               |
| :-------------- | :------ | :--------------- |
| `ths_hot_top`   | 同花顺热度排行 | `date1`, `top_n` |
| `stock_ths_hot` | 个股同花顺热度 | `code`, `date1`  |

### 个股数据

| 方法名                            | 描述   | 参数                               |
| :----------------------------- | :--- | :------------------------------- |
| `stock_uplimit_reason`         | 涨停原因 | `stock_code`, `date`             |
| `stock_uplimit_reason_history` | 涨停历史 | `stock_code`, `page`, `pageSize` |
| `stock_info`                   | 个股信息 | `stock_id`, `info_type`          |
| `stock_moneyflow`              | 资金流向 | `stock_id`, `m_type`             |

### 龙虎榜

| 方法名                  | 描述      | 参数                                                           |
| :------------------- | :------ | :----------------------------------------------------------- |
| `lhb_list`           | 龙虎榜列表   | `date1`                                                      |
| `lhb_detail`         | 龙虎榜详情   | `date1`, `stock_code`                                        |
| `lhb_stock_history`  | 个股龙虎榜历史 | `stock_code`, `trader_name`                                  |
| `lhb_trader_history` | 席位交易历史  | `trader_name`, `trader_id`, `stock_code`, `page`, `per_page` |

### 实时数据

| 方法名           | 描述     | 参数                                 |
| :------------ | :----- | :--------------------------------- |
| `market_mf`   | 资金流向分钟 | `stock`, `date`, `wm`, `default_v` |

### 其他

| 方法名                      | 描述       | 参数                                  |
| :----------------------- | :------- | :---------------------------------- |
| `uplimit_market_value`   | 涨停市值统计   | `date1`, `date2`                    |
| `sentiment_market_top_n` | 市场TopN情绪 | `modal_id`, `date1`, `date2`        |
| `movement_alerts`        | 异动数据     | `date1`, `type`, `limit`, `is_real` |
| `zdjk_get`               | 监控数据     | `date1`, `date2`                    |

</details>

***

## 🔧 通用查询

使用 `query` 方法可以调用任意自定义接口：

```python
result = api.query('your/custom/path', params={'key': 'value'})
```

***

# ✅ 安装 AI Agent (MCP) 扩展支持

```bash
pip install "zzshare[mcp]"

```

***

## 🤖 For AI Agents & LLMs (MCP 全球服务)

`zzshare` 原生支持 **Model Context Protocol (MCP)**。我们精心调优了其在 LLM 上下文环境中的表现，通过 Token 防御与动态 Schema 给大模型带来最佳的零代码获取量化数据体验。

如果你是一名在 **Claude Desktop, Cursor, Zed** 等支持 MCP 协议的软件中的开发者，只需在相关配置中添加如下配置，即可解锁数十个股市查询能力（向 AI 提问如：“今日涨停榜分析” 或 “打印 600519 最近一周走势”）：

**适用于 Claude Desktop 的配置 (`claude_desktop_config.json`)**:

```json
{
  "mcpServers": {
    "zzshare-quant": {
      "command": "zzshare-mcp",
      "args": [],
      "env": {
        "ZZSHARE_TOKEN": "YOUR_API_TOKEN_HERE" // 您可以在 https://quant.zizizaizai.com 获取
      }
    }
  }
}
```

如果你是在终端构建 AI 智能体（如 GStack Agent / OpenCode），可直接使用我们提供的 `zzshare-cli` 控制台工具进行快速提数。

***

## 💡 AI Agent 使用秘籍 (Pro Tips)

为了让大模型更好地为您提供量化分析建议，我们建议在提示词中加入以下技巧：

### 1. 自动处理非交易日 (Self-Correction)

`zzshare` 内置了**大模型私语 (Secret Prompting)**。当模型查询的数据返回为空时（通常因为当天是周六日或节假日），系统会自动提示模型：“*数据为空，请核实是否为交易日*”。
> **推荐 Prompt**: "如果数据返回为空，请先调用 `trade_days` 检查最近的开盘日期，并以此自动调整查询范围。"

### 2. 语义化工具发现

所有的接口都已配备了**语义化描述**。模型可以清晰地分辨什么是“龙虎榜席位分析”，什么是“市场情绪分布”。
> **示例指令**: "分析一下今天全市场的涨跌停分布，并列出排名前三的热点板块及其领涨股。"

### 3. Token 防御机制

无需担心金融大表刷屏导致上下文崩溃。`zzshare` 会自动对长表格进行双端截断并转换为 Markdown，确保大模型始终能看到最新的走势和表头信息。

***

## ❓ 常见问题

<details>
<summary><b>Q: 需要申请 Token 吗？</b></summary>
大部分不需要，但是为了保障接口稳定性，zzshare 部分接口需要 API Token。
您可以在 [个人中心](https://api.zizizaizai.com/user/profile) 免费获取初始 Token。

</details>

<details>
<summary><b>Q: 数据更新频率？</b></summary>

- 日线数据：每日收盘后更新
- 涨停/龙虎榜：每日收盘后更新
- 实时数据：盘中实时

</details>

<details>
<summary><b>Q: 支持哪些 Python 版本？</b></summary>

Python 3.8+

</details>

***

## 📄 License

MIT License

***

<p align="center">
  ⭐ 如果这个项目对你有帮助，请给它一个 Star！
</p>
