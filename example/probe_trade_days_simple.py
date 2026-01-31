import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from zzshare import DataApi
import pandas as pd

api = DataApi()

print("--- Testing trade_days simplified ---")
try:
    df = api.trade_days(start_date='20251208', end_date='2025-12-15')
    print("Type:", type(df))
    print(df)
except Exception as e:
    print(f"Error: {e}")
