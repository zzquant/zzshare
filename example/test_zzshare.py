
print("Starting test...")
import sys
import os

# Add workspace to path to import zzshare package
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

try:
    import zzshare as zz
    print("Imported zzshare")
except ImportError as e:
    print(f"Import Error: {e}")
    sys.exit(1)

def test():
    print("Initializing API...")
    pro = zz.pro_api()
    
    print("--- Testing Daily (000001.SZ) ---")
    try:
        df = pro.daily(symbol_code='000001.SZ', start_date='2024-12-01', end_date='2025-12-30')
        if not df.empty:
            print(df[['trade_date', 'open', 'close', 'pct_chg']].head())
            print(df[['trade_date', 'open', 'close', 'pct_chg']].tail())
        else:
            print("Empty DataFrame returned for Daily")
    except Exception as e:
        print(f"Daily Error: {e}")
    
    print("\n--- Testing Limit List (20241226) ---")
    try:
        df_limit = pro.limit_list(trade_date='20241226')
        if not df_limit.empty:
            print(df_limit[['trade_date', 'symbol_code', 'name', 'limit_reason', 'limit_status']].head())
        else:
            print("Empty DataFrame returned for Limit List")
    except Exception as e:
        print(f"Limit List Error: {e}")

    print("\n--- Testing Trade Days (20251201-20251231) ---")
    try:
        df_cal = pro.trade_days(start_date='20251201', end_date='20251231')
        if not isinstance(df_cal, list) and not df_cal.empty:
            print(df_cal.head(10))
            print(f"Total days: {len(df_cal)}")
        elif isinstance(df_cal, list):
            print(f"Trade Days List: {df_cal}")
        else:
            print("Empty DataFrame returned for Trade Days")
    except Exception as e:
        print(f"Trade Days Error: {e}")

    print("\n--- Testing Stock Basic (Placeholder) ---")
    try:
        df_basic = pro.stock_basic()
        print(f"Stock Basic Columns: {df_basic.columns.tolist()}")
        print(f"Stock Basic Empty: {df_basic.empty}")
    except Exception as e:
        print(f"Stock Basic Error: {e}")

    print("\n--- Testing Daily Basic (TODO) ---")
    try:
        df_db = pro.daily_basic()
        print(f"Daily Basic Empty: {df_db.empty}")
    except Exception as e:
        print(f"Daily Basic Error: {e}")

    print("\n--- Testing New Placeholders (e.g. trade_days) ---")
    try:
        df_cal = pro.trade_days()
        print(f"Trade Days Empty: {not df_cal if isinstance(df_cal, list) else df_cal.empty}")
    except Exception as e:
        print(f"Trade Days Error: {e}")

if __name__ == "__main__":
    test()
