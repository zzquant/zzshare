# -*- coding: utf-8 -*-
import argparse
import sys
import json
from zzshare.client import DataApi
from zzshare.ai_utils import format_to_llm

def main():
    parser = argparse.ArgumentParser(
        description="zzshare 量化数据终端 - 供开发者与 AI Agent 快速调用的命令行工具"
    )
    
    # 动态构建子命令
    subparsers = parser.add_subparsers(dest="command", help="支持的量化数据接口")
    
    # 手动添加几个核心的，方便给更好的 help
    daily_parser = subparsers.add_parser("daily", help="获取日线行情数据")
    daily_parser.add_argument("--ts_code", type=str, help="股票代码, e.g., 000001.SZ")
    daily_parser.add_argument("--trade_date", type=str, help="交易日期 YYYYMMDD")
    daily_parser.add_argument("--start_date", type=str, help="起始日期")
    daily_parser.add_argument("--limit", type=int, help="数量限制")
    daily_parser.add_argument("--offset", type=int, help="偏移量")

    # Mins
    mins_parser = subparsers.add_parser("stk_mins", help="获取分钟级 K 线数据")
    mins_parser.add_argument("--ts_code", type=str, required=True, help="股票代码, e.g., 600519.SH")
    mins_parser.add_argument("--freq", type=str, default="1min", help="频率: 1min, 5min, 15min, 30min, 60min")
    mins_parser.add_argument("--start_time", type=str, help="开始时间 YYYYMMDDHHMM")
    mins_parser.add_argument("--end_time", type=str, help="结束时间 YYYYMMDDHHMM")
    mins_parser.add_argument("--limit", type=int, help="数量限制")

    # Stock Basic
    basic_parser = subparsers.add_parser("stock_basic", help="获取股票基础信息")
    basic_parser.add_argument("--ts_code", type=str, help="股票代码")
    basic_parser.add_argument("--name", type=str, help="股票名称(支持模糊查询)")
    
    # 动态把 SHORTCUTS 塞进 CLI
    for name, entry in DataApi.SHORTCUTS.items():
        if name in ["daily", "stock_basic", "stk_mins"]: 
            continue
            
        if len(entry) == 4:
            _, param_list, _, desc = entry
        else:
            _, param_list, _ = entry
            desc = f"动态接口: {name}"

        cmd_parser = subparsers.add_parser(name, help=desc)
        for p in param_list:
            cmd_parser.add_argument(f"--{p}", type=str, help=f"参数: {p}")
            
    # 全局参数
    parser.add_argument("--format", choices=["markdown", "json"], default="markdown", help="输出格式")
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        sys.exit(1)
        
    # 组装 kwargs
    kwargs = {}
    args_dict = vars(args)
    for k, v in args_dict.items():
        if k not in ["command", "format"] and v is not None:
            kwargs[k] = v
            
    api = DataApi()
    try:
        # 调用
        method = getattr(api, args.command)
        res = method(**kwargs)
        
        if args.format == 'markdown':
            # 使用 AI Utils 转换（会自动截断过长的表防止刷爆控制台）
            print(format_to_llm(res, max_rows=100))
        else:
            # 完整输出 JSON
            import pandas as pd
            if isinstance(res, pd.DataFrame):
                print(res.to_json(orient="records", force_ascii=False))
            else:
                print(json.dumps(res, ensure_ascii=False, indent=2))
                
    except Exception as e:
        print(f"执行失败: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
