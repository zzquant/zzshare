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
    daily_parser = subparsers.add_parser(
        "daily", 
        help="获取日线行情数据",
        description="获取 A 股日线行情。支持单股历史区间查询和全市场特定交易日快照查询。",
        epilog="注意：API 能够获取的数据量取决于 limit 参数(1-1000)；为保护上下文，CLI 打印时超过 1000 行将自动截断。"
    )
    daily_parser.add_argument("--ts_code", type=str, help="股票代码, e.g., 000001.SZ")
    daily_parser.add_argument("--start_date", type=str, help="起始日期")
    daily_parser.add_argument("--end_date", type=str, help="结束日期")
    daily_parser.add_argument("--trade_date", type=str, help="交易日期 YYYYMMDD")
    daily_parser.add_argument("--limit", type=int, help="数量限制。获取全市场快照时建议 1-6000；获取单股区间时取值范围(1-1000，默认 1000)。注意：超过 1000 条输出将智能截断。获取更多需要配合 offset 参数分页获取。")
    daily_parser.add_argument("--offset", type=int, help="偏移量。配合 limit 分页使用，取值范围为 >= 0 的整数(0-1000)。比如按照每次取1000条, 第二页offset=1000,limit=1000")

    # Mins 
    mins_parser = subparsers.add_parser("stk_mins", help="获取分钟级 K 线数据")
    mins_parser.add_argument("--ts_code", type=str, required=True, help="股票代码, e.g., 600519.SH")
    mins_parser.add_argument("--freq", type=str, default="1min", help="频率: 1min, 5min, 15min, 30min, 60min")
    mins_parser.add_argument("--start_time", type=str, help="开始时间 YYYYMMDDHHMM")
    mins_parser.add_argument("--end_time", type=str, help="结束时间 YYYYMMDDHHMM")
    mins_parser.add_argument("--limit", type=int, help="数量限制")

    # Plates Rank
    pr_parser = subparsers.add_parser("plates_rank", help="获取全市场所有板块的热度排名")
    pr_parser.add_argument("--plate_type", type=int, required=True, help="板块类型 (17:题材, 15:概念, 14:行业)")
    pr_parser.add_argument("--date1", type=str, required=True, help="查询日期 (YYYYMMDD)")
    pr_parser.add_argument("--limit", type=int, default=10, help="返回条数")

    # Plates Rank Days
    prd_parser = subparsers.add_parser("plates_rank_days", help="查询板天内块排名数据(区间排名)")
    prd_parser.add_argument("--plate_type", type=int, required=True, help="板块类型 (17:题材, 15:概念, 14:行业)")
    prd_parser.add_argument("--date2", type=str, required=True, help="截止日期 (YYYYMMDD)")
    prd_parser.add_argument("--n_days", type=int, default=5, help="累计天数")
    prd_parser.add_argument("--n_type", type=int, default=3, help="排序类型 (1:涨幅, 3:净额, 9:强度)")
    prd_parser.add_argument("--limit", type=int, default=10, help="返回条数")

    # Plates Rank Days New
    prdn_parser = subparsers.add_parser("plates_rank_days_new", help="获取指定板块Top N，并标记是否是前几天新进的")
    prdn_parser.add_argument("--plate_type", type=int, required=True, help="板块类型 (17:题材, 15:概念, 14:行业)")
    prdn_parser.add_argument("--date2", type=str, required=True, help="截止日期 (YYYYMMDD)")
    prdn_parser.add_argument("--n_days", type=int, default=5, help="累计天数")
    prdn_parser.add_argument("--n_type", type=int, default=3, help="排序类型 (1:涨幅, 3:净额, 9:强度)")
    prdn_parser.add_argument("--limit", type=int, default=20, help="返回条数")
    prdn_parser.add_argument("--prev_days", type=int, default=3, help="对比前几日天数")

    # Sentiment Trend
    st_parser = subparsers.add_parser("sentiment_trend", help="基于特定模型计算的市场情绪分时数据(单日)")
    st_parser.add_argument("--model", type=int, required=True, help="情绪模型 ID (0:综合情绪, 20:市场热度, 1:接力情绪)")
    st_parser.add_argument("--date1", type=str, help="查询日期 (YYYYMMDD)")

    # Sentiment Trend Range
    str_parser = subparsers.add_parser("sentiment_trend_range", help="基于特定模型计算的市场情绪分时数据(多日区间)")
    str_parser.add_argument("--model", type=int, required=True, help="情绪模型 ID (0:综合情绪, 20:市场热度, 1:接力情绪)")
    str_parser.add_argument("--date1", type=str, required=True, help="开始日期 (YYYYMMDD)")
    str_parser.add_argument("--date2", type=str, required=True, help="结束日期 (YYYYMMDD)")

    # Market Sentiment (K-Line)
    ms_parser = subparsers.add_parser("market_sentiment", help="综合市场情绪数据量化出来的 K 线数据")
    ms_parser.add_argument("--date1", type=str, required=True, help="开始日期 (YYYYMMDD)")
    ms_parser.add_argument("--date2", type=str, help="结束日期 (YYYYMMDD)")

    # Market Hot Sentiment (K-Line)
    mhs_parser = subparsers.add_parser("market_hot_sentiment", help="市场热度数据量化出来的 K 线数据")
    mhs_parser.add_argument("--date1", type=str, required=True, help="开始日期 (YYYYMMDD)")
    mhs_parser.add_argument("--date2", type=str, help="结束日期 (YYYYMMDD)")

    # Market Plate Popular Reason
    mppr_parser = subparsers.add_parser("market_plate_popular_reason", help="获取板块题材的爆点/原因列表")
    mppr_parser.add_argument("--plate_code", type=str, required=True, help="板块代码")
    mppr_parser.add_argument("--date2", type=str, help="截止日期 (YYYYMMDD)")

    # Review Uplimit Hot (Open)
    ruho_parser = subparsers.add_parser("review_uplimit_hot_step", help="指定板块下的涨停梯队数据")
    ruho_parser.add_argument("--date1", type=str, help="查询日期 (YYYYMMDD)")
    ruho_parser.add_argument("--board", type=str, help="板块代码")
    ruho_parser.add_argument("--limit", type=int, help="数量限制")

    # Stock Basic
    basic_parser = subparsers.add_parser("stock_basic", help="获取股票基础信息")
    basic_parser.add_argument("--ts_code", type=str, help="股票代码")
    basic_parser.add_argument("--name", type=str, help="股票名称(支持模糊查询)")
    
    # THS Hot Top
    tht_parser = subparsers.add_parser("ths_hot_top", help="获取同花顺热搜榜前 N 名龙头的实时排名")
    tht_parser.add_argument("--date1", type=str, help="查询日期 (YYYYMMDD)")
    tht_parser.add_argument("--top_n", type=int, default=10, help="返回前 N 名")
    
    # 动态把 SHORTCUTS 塞进 CLI
    for name, entry in DataApi.SHORTCUTS.items():
        if name in [
            "daily", "stock_basic", "stk_mins", "plates_rank", "plates_rank_days", "plates_rank_days_new", 
            "sentiment_trend", "sentiment_trend_range", "market_sentiment", "market_hot_sentiment", 
            "market_plate_popular_reason", "review_uplimit_hot_step", "ths_hot_top"
        ]: 
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
            print(format_to_llm(res))
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
