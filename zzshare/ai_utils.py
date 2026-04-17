# -*- coding: utf-8 -*-
import pandas as pd
from typing import Dict, Any, Type, Optional, List

def format_to_llm(data: Any, max_rows: int = 50) -> str:
    """
    将 API 返回的数据转换为对 LLM 友好的格式（主要处理 DataFrame 转 Markdown）。
    加入防爆截断（Token Protection）。
    """
    if data is None or (isinstance(data, (list, pd.DataFrame)) and len(data) == 0):
        return (
            "数据为空 (Empty Data)。\n\n"
            "💡 [系统建议] 如果返回为空，请确认查询日期是否为交易日（非周六日/节假日）。"
            "您可以尝试调用 `trade_days` 接口核实最近的交易日期范围。"
        )

    if isinstance(data, list) and isinstance(data[0], dict):
        df = pd.DataFrame(data)
    elif isinstance(data, pd.DataFrame):
        df = data
    else:
        # 非表格数据直接返回
        return str(data)

    if df.empty:
        return (
            "数据为空 (Empty Data)。\n\n"
            "💡 [系统建议] 如果返回为空，请确认查询日期是否为交易日（非周六日/节假日）。"
            "您可以尝试调用 `trade_days` 接口核实最近的交易日期范围。"
        )

    total_rows = len(df)
    if total_rows > max_rows:
        head_rows = max_rows // 2
        tail_rows = max_rows - head_rows
        head_df = df.head(head_rows)
        tail_df = df.tail(tail_rows)
        
        md_head = head_df.to_markdown(index=False)
        # 去掉 tail 表格的 title 行以保持连续性体验（也可保留）
        md_tail = tail_df.to_markdown(index=False)
        
        return (
            f"⚠️ **注意：数据量过大 ({total_rows} 行)，已智能截取首尾 {max_rows} 行以保护上下文。**\n\n"
            f"{md_head}\n"
            f"...\n"
            f"... [省略 {total_rows - max_rows} 行数据，请引导用户缩短 start_date/end_date 或使用 offset/limit 分页获取] ...\n"
            f"...\n"
            f"{md_tail}\n\n"
            f"💡 提示大模型：您可以根据上述抽样数据给出趋势分析，若需精准数据计算，请调整查询的时间窗口。"
        )
    else:
        return df.to_markdown(index=False)


# 参数推断提示工厂 (Semantic Typing)
def get_param_annotation(param_name: str) -> str:
    """推断常用量化参数的类型与描述"""
    annotations = {
        "ts_code": "股票代码，需带后缀，例如 000001.SZ, 600519.SH",
        "trade_date": "交易日期，格式 YYYYMMDD，如 '20260416'",
        "start_date": "开始日期，格式 YYYYMMDD，如 '20260401'",
        "end_date": "结束日期，格式 YYYYMMDD，如 '20260416'",
        "limit": "返回数据最大条数，默认返回全部或限制",
        "offset": "返回数据的起始偏移量，用于分页",
        "is_real": "是否获取实时数据（通常 1 为是，0 为否）",
        "day_start": "开始日期，格式 YYYYMMDD",
        "day_end": "结束日期，格式 YYYYMMDD",
        "date1": "日期参数1，格式 YYYYMMDD",
        "date2": "日期参数2，格式 YYYYMMDD",
        "date": "具体日期，格式 YYYYMMDD",
        "board": "板块参数",
        "plate_code": "板块代码",
        "plate_type": "板块分类类型",
        "stock_code": "股票代码",
        "st": "包含 ST 状态筛选",
    }
    return annotations.get(param_name, f"参数 {param_name}")

