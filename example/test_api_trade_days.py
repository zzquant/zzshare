import requests
import json

base_url = "http://127.0.0.1:9001/market/trade/days"

def test_default():
    print("--- Testing Default (days=5) ---")
    try:
        resp = requests.get(base_url, params={'days': 5})
        print(f"Status: {resp.status_code}")
        data = resp.json()
        print(json.dumps(data, indent=2, ensure_ascii=False))
    except Exception as e:
        print(f"Error: {e}")

def test_range():
    print("\n--- Testing Range (2025-12-08 to 2025-12-19) ---")
    try:
        params = {
            'day_start': '2025-12-08',
            'day_end': '2025-12-19'
        }
        resp = requests.get(base_url, params=params)
        print(f"Status: {resp.status_code}")
        data = resp.json()
        print(json.dumps(data, indent=2, ensure_ascii=False))
    except Exception as e:
        print(f"Error: {e}")

def test_mixed_formats():
    print("\n--- Testing Mixed Formats (20251208 to 2025-12-19) ---")
    try:
        params = {
            'day_start': '20251208',
            'day_end': '2025-12-19'
        }
        resp = requests.get(base_url, params=params)
        print(f"Status: {resp.status_code}")
        data = resp.json()
        print(json.dumps(data, indent=2, ensure_ascii=False))
    except Exception as e:
        print(f"Error: {e}")

def test_invalid_format():
    print("\n--- Testing Invalid Format (2025-13-45) ---")
    try:
        params = {
            'day_start': '2025-13-45',
            'day_end': '2025-12-19'
        }
        resp = requests.get(base_url, params=params)
        print(f"Status: {resp.status_code}")
        data = resp.json()
        print(json.dumps(data, indent=2, ensure_ascii=False))
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    test_default()
    test_range()
    test_mixed_formats()
    test_invalid_format()
