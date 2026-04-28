# -*- coding: utf-8 -*-
import os
import asyncio
from typing import Any, Dict, List, Optional
from mcp.server.fastmcp import FastMCP
import mcp.types as types

from zzshare import daily, stock_basic
from zzshare.client import DataApi
from zzshare.core import ApiAuthError, ApiRateLimitError
from zzshare.ai_utils import format_to_llm, get_param_annotation
from zzshare.logger import logger

# ========= 初始化 MCP 服务 =========
mcp = FastMCP("zzshare-quant")

# ========= 静态高频工具 (精心打磨 Prompt) =========

@mcp.tool()
def get_daily_market_data(
    ts_code: str = None, 
    trade_date: str = None, 
    start_date: str = None, 
    end_date: str = None, 
    limit: int = 1000,
    offset: int = 0
) -> str:
    """
    获取 A 股全市场或单只股票的日线级别的历史 K 线数据。
    
    参数说明:
    - ts_code: 股票代码，需带后缀，例如 '000001.SZ'。如果为空，将拉取全市场数据。
    - trade_date: 特定交易日，格式 YYYYMMDD，如 '20260416'。
    - start_date: 开始日期，格式 YYYYMMDD。
    - end_date: 结束日期，格式 YYYYMMDD。
    - limit: 返回条数。单股上限 1000（默认 1000），全市场上限 10000（建议 6000）。
    - offset: 偏移量，用于分页获取更深的历史数据（每页建议 1000）。
    
    返回:
    Markdown 表格格式的日线数据。
    """
    try:
        # SDK 原生支持：若查询失败会抛出 ApiRateLimitError 等
        df = daily(ts_code=ts_code, trade_date=trade_date, start_date=start_date, end_date=end_date, limit=limit, offset=offset)
        return format_to_llm(df)
    except ApiRateLimitError as e:
        return str(e)
    except ApiAuthError as e:
        return str(e)
    except Exception as e:
        return f"接口执行异常: {e}"


@mcp.tool()
def get_stock_basic_info(ts_code: str = None, name: str = None) -> str:
    """
    获取股票的基础信息列表，包括 TS 代码、股票名称、上市状态等。
    可用于通过公司全称（包含在name内）模糊查询股票的 TS 代码。
    例如：查询“贵州茅台”的代码，设置 name='茅台'。
    """
    try:
        df = stock_basic(ts_code=ts_code, name=name)
        return format_to_llm(df)
    except Exception as e:
        return f"接口执行异常: {e}"


@mcp.tool()
def get_minute_market_data(
    ts_code: str,
    start_time: str = None,
    end_time: str = None,
    freq: str = "1min",
    limit: int = 100
) -> str:
    """
    获取股票的分钟级别 K 线数据。建议在需要观察盘中精细走势时使用。
    
    参数:
    - ts_code: 股票代码 (e.g., '000001.SZ')
    - start_time: 开始时间，格式 YYYYMMDDHHMM (可选)
    - end_time: 结束时间，格式 YYYYMMDDHHMM (可选)
    - freq: 分钟频率，支持 '1min', '5min', '15min', '30min', '60min'
    - limit: 返回数据量限制
    """
    api = DataApi()
    try:
        df = api.stk_mins(ts_code=ts_code, start_time=start_time, end_time=end_time, freq=freq, limit=limit)
        return format_to_llm(df)
    except Exception as e:
        return f"接口执行异常: {e}"


# ========= 动态工具注册引擎 =========
# 考虑到 FastMCP 需要函数签名进行自省，我们动态生成包裹函数并注册。

def _create_dynamic_mcp_tool(shortcut_name: str, params_list: List[str], desc: str):
    # 生成函数的 Docstring
    docstring = f"{desc}\n\n参数列表:\n"
    for p in params_list:
        docstring += f"- {p}: {get_param_annotation(p)}\n"
        
    def dynamic_tool(**kwargs: str) -> str:
        api = DataApi()
        try:
            method = getattr(api, shortcut_name)
            res = method(**kwargs)
            return format_to_llm(res)
        except ApiRateLimitError as e:
            return str(e)
        except ApiAuthError as e:
            return str(e)
        except Exception as e:
            return f"调用失败: {e}"
            
    dynamic_tool.__name__ = f"quant_api_{shortcut_name}"
    dynamic_tool.__doc__ = docstring
    
    # 注册到 FastMCP
    mcp.add_tool(dynamic_tool)

# 自动扫描 DataApi.SHORTCUTS 并注册
for name, entry in DataApi.SHORTCUTS.items():
    if name in ["daily", "stock_basic"]:
        continue
        
    if len(entry) == 4:
        _, p_list, _, desc = entry
    else:
        # 兼容旧格式
        _, p_list, _ = entry
        desc = name
        
    _create_dynamic_mcp_tool(name, p_list, desc)

def main():
    logger.info("启动 zzshare MCP Server ... 监听标准输入输出(stdio)")
    mcp.run(transport='stdio')

if __name__ == '__main__':
    main()
