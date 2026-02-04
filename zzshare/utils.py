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
