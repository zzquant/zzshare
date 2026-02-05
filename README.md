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

---

## ✨ 特性

- 🚀 **开箱即用** - 无需申请 Token，安装即可使用
- 📊 **丰富数据** - 涨停复盘、龙虎榜、情绪指标、板块热度等 40+ 接口
- 🔄 **兼容 tushare** - 接口规范兼容 tushare pro，迁移成本低
- ⚡ **实时数据** - 支持实时行情、资金流向等盘中数据
- 🐍 **类型提示** - 完整的 `.pyi` 类型文件，IDE 自动补全

---

## 📦 安装

```bash
pip install git+https://github.com/zzquant/zzshare.git
```

或克隆后本地安装：

```bash
git clone https://github.com/zzquant/zzshare.git
cd zzshare
pip install -e .
```

---

## 🚀 快速开始

**3 行代码获取数据：**

```python
from zzshare.client import DataApi

api = DataApi()

# 获取日线行情
df = api.daily(code='000001', date1='20250101', date2='20250131')
print(df)
```

**更多示例：**

```python
# 获取今日涨停热门板块
hot = api.uplimit_hot(date1='20250205')

# 获取龙虎榜
lhb = api.lhb_list(date1='20250205')

# 获取同花顺热度 Top 100
ths_top = api.ths_hot_top(date1='20250205', top_n=100)

# 获取交易日历
days = api.trade_days(days=30)
```

---

## 📊 接口一览

### 核心接口 (已实现)

| 分类 | 接口 | 描述 |
|:---|:---|:---|
| **日线数据** | `daily` | 个股日K线，返回 DataFrame |
| **涨停复盘** | `uplimit_hot` `uplimit_stocks` | 涨停热门板块、涨停股票 |
| **涨停原因** | `stock_uplimit_reason` `review_uplimit_reason` | 个股/全市场涨停原因 |
| **龙虎榜** | `lhb_list` `lhb_detail` `lhb_stock_history` | 龙虎榜列表、详情、历史 |
| **板块数据** | `plates_list` `plates_rank` `market_plate` | 板块列表、排名、热门 |
| **情绪指标** | `market_sentiment` `sentiment_trend` `sentiment_level` | 市场情绪K线、趋势、级别 |
| **热度数据** | `ths_hot_top` `stock_ths_hot` | 同花顺热度排行、个股热度 |
| **实时行情** | `market_real` `stock_moneyflow` | 实时快照、资金流向 |
| **基础数据** | `trade_days` `stock_info` | 交易日历、个股信息 |

> 💡 共计 **40+** 个已实现接口，完整列表见下方。

---

## 📖 使用示例

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

### 实时数据

```python
# 获取多只股票实时行情
real = api.market_real(symbols='000001,000002,000003')
```

---

## 📚 完整接口列表

<details>
<summary><b>点击展开全部接口</b></summary>

### 复盘数据
| 方法名 | 描述 | 参数 |
|:---|:---|:---|
| `uplimit_hot` | 涨停热门板块 | `date1`, `board` |
| `uplimit_stocks` | 涨停股票列表 | `date1` |
| `review_uplimit_reason` | 涨停原因复盘 | `date1`, `group`, `page`, `page_size` |
| `review_uplimit_hot_open` | 涨停热门 | `date1`, `date2`, `board`, `limit` |
| `review_uplimit_reason_open` | 涨停原因 | `date1` |

### 情绪数据
| 方法名 | 描述 | 参数 |
|:---|:---|:---|
| `market_sentiment` | 市场情绪K线 | `date1`, `date2` |
| `market_hot_sentiment` | 热门情绪K线 | `date1`, `date2` |
| `market_style` | 市场风格择时 | `date1` |
| `open_sentiment_data` | 情绪数据 | `date1`, `date2` |
| `sentiment_market_hot_day` | 当日市场热度 | `date` |
| `sentiment_trend` | 情绪趋势 | `model`, `date1` |
| `sentiment_trend_range` | 情绪趋势区间 | `model`, `date1`, `date2` |
| `updown_distribution` | 涨跌分布 | `date1` |
| `uplimit_trend` | 涨停趋势 | `date1` |
| `sentiment_hot_day` | 日度市场热度 | `index`, `st` |
| `sentiment_level` | 情绪级别 | `date` |
| `sentiment_bull_data` | 牛熊情绪 | `date1`, `date2` |

### 板块数据
| 方法名 | 描述 | 参数 |
|:---|:---|:---|
| `market_plate` | 板块排行 | `date1`, `limit` |
| `market_plate_stocks` | 板块成分股排行 | `plate_code`, `date1`, `is_real`, `limit` |
| `plates_list` | 板块列表 | `plate_type` |
| `plates_rank` | 板块排名 | `plate_type`, `date1`, `limit` |
| `plates_trend` | 板块趋势 | `plate_type`, `plate_code`, `day_start`, `day_end` |
| `plates_stocks` | 板块成分股 | `plate_type`, `plate_code`, `date` |

### K线数据
| 方法名 | 描述 | 参数 | 返回 |
|:---|:---|:---|:---|
| `daily` | 日线行情 | `code`, `date1`, `date2` | DataFrame |

### 基础数据
| 方法名 | 描述 | 参数 |
|:---|:---|:---|
| `trade_days` | 交易日历 | `day_start`, `day_end`, `days` |

### 热度数据
| 方法名 | 描述 | 参数 |
|:---|:---|:---|
| `ths_hot_top` | 同花顺热度排行 | `date1`, `top_n` |
| `stock_ths_hot` | 个股同花顺热度 | `code`, `date1` |

### 个股数据
| 方法名 | 描述 | 参数 |
|:---|:---|:---|
| `stock_uplimit_reason` | 涨停原因 | `stock_code`, `date` |
| `stock_uplimit_reason_history` | 涨停历史 | `stock_code`, `page`, `pageSize` |
| `stock_info` | 个股信息 | `stock_id`, `info_type` |
| `stock_moneyflow` | 资金流向 | `stock_id`, `m_type` |

### 龙虎榜
| 方法名 | 描述 | 参数 |
|:---|:---|:---|
| `lhb_list` | 龙虎榜列表 | `date1` |
| `lhb_detail` | 龙虎榜详情 | `date1`, `stock_code` |
| `lhb_stock_history` | 个股龙虎榜历史 | `stock_code`, `trader_name` |
| `lhb_trader_history` | 席位交易历史 | `trader_name`, `trader_id`, `stock_code`, `page`, `per_page` |

### 实时数据
| 方法名 | 描述 | 参数 |
|:---|:---|:---|
| `market_real` | 行情实时快照 | `symbols` |
| `market_mf` | 资金流向分钟 | `stock`, `date`, `wm`, `default_v` |

### 其他
| 方法名 | 描述 | 参数 |
|:---|:---|:---|
| `uplimit_market_value` | 涨停市值统计 | `date1`, `date2` |
| `sentiment_market_top_n` | 市场TopN情绪 | `modal_id`, `date1`, `date2` |
| `movement_alerts` | 异动数据 | `date1`, `type`, `limit`, `is_real` |
| `zdjk_get` | 监控数据 | `date1`, `date2` |

</details>

---

## 🔧 通用查询

使用 `query` 方法可以调用任意自定义接口：

```python
result = api.query('your/custom/path', params={'key': 'value'})
```

---

## ❓ 常见问题

<details>
<summary><b>Q: 需要申请 Token 吗？</b></summary>

不需要！zzshare 开箱即用，无需申请任何 Token。

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

---

## 📄 License

MIT License

---

<p align="center">
  ⭐ 如果这个项目对你有帮助，请给它一个 Star！
</p>
