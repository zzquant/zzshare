import pandas as pd


def kline_data_to_df(data):
    if not data:
        return pd.DataFrame()

    dates = data.get('x', [])
    y_data = data.get('y', [])
    vols = data.get('vol', [])
    amounts = data.get('business_balance', [])

    records = []
    for i, date_str in enumerate(dates):
        if i >= len(y_data):
            break
        y = y_data[i]
        if len(y) < 5:
            continue

        open_px = y[0]
        close_px = y[1]
        high_px = y[2]
        low_px = y[3]
        pre_close = y[4]
        vol = vols[i] if i < len(vols) else 0
        amount = amounts[i] if i < len(amounts) else 0

        change = close_px - pre_close if pre_close else 0
        pct_chg = (change / pre_close * 100) if pre_close else 0

        records.append({
            'trade_date': str(date_str).replace('-', ''),
            'open': open_px,
            'high': high_px,
            'low': low_px,
            'close': close_px,
            'pre_close': pre_close,
            'change': round(change, 4),
            'pct_chg': round(pct_chg, 4),
            'vol': vol,
            'amount': amount
        })

    return pd.DataFrame(records)


def plate_kline_to_df(data):
    if not data:
        return pd.DataFrame()
    df = pd.DataFrame(data)
    if not df.empty:
        # 兼容多种日期列名
        for col in ['date', 'trade_date', 'date1']:
            if col in df.columns:
                df['trade_date'] = pd.to_datetime(df[col]).dt.strftime('%Y%m%d')
                break
    return df


def finance_data_to_df(data):
    if not data:
        return pd.DataFrame()
    return pd.DataFrame(data)


def trend_data_to_df(data):
    """
    将个股或板块的分钟级分时数据转换为 DataFrame。
    包含时间、点位/价格、分时均价、成交量、成交额、涨跌额、涨跌幅等。
    """
    if not data:
        return pd.DataFrame()

    vol_amt_map = {}
    if isinstance(data, dict):
        trend_list = data.get('trend', [])
        code = str(data.get('code', ''))
        day = str(data.get('day', '')).replace('-', '')
        preclose = float(data.get('preclose_px') or 0.0)
        vol_amt_list = data.get('volumeturnover', [])
        if vol_amt_list:
            for v_item in vol_amt_list:
                if isinstance(v_item, (list, tuple)) and len(v_item) >= 3:
                    vol_amt_map[str(v_item[0])] = (float(v_item[1]), float(v_item[2]))
    elif isinstance(data, list):
        trend_list = data
        code = ''
        day = ''
        preclose = 0.0
    else:
        return pd.DataFrame()

    records = []
    for item in trend_list:
        if not isinstance(item, (list, tuple)) or len(item) < 2:
            continue
        t_time = str(item[0])
        px = float(item[1]) if item[1] is not None else None
        avg_px = float(item[2]) if len(item) > 2 and item[2] is not None else 0.0
        vol = float(item[3]) if len(item) > 3 and item[3] is not None else 0.0
        direction = int(item[4]) if len(item) > 4 and item[4] is not None else 0

        amount = 0.0
        if t_time in vol_amt_map:
            v_mapped, amt_mapped = vol_amt_map[t_time]
            if vol == 0.0:
                vol = v_mapped
            amount = amt_mapped
        elif avg_px > 0 and vol > 0:
            amount = round(avg_px * vol * 100, 2)

        change = round(px - preclose, 4) if preclose and px is not None else 0.0
        pct_chg = round((px - preclose) / preclose * 100, 3) if preclose and px is not None else 0.0

        trade_time_str = f"{day[:4]}-{day[4:6]}-{day[6:8]} {t_time}:00" if len(day) == 8 else t_time

        records.append({
            'code': code,
            'trade_time': trade_time_str,
            'time': t_time,
            'price': px,
            'avg_price': avg_px,
            'vol': vol,
            'amount': amount,
            'direction': direction,
            'change': change,
            'pct_chg': pct_chg,
        })

    return pd.DataFrame(records)
