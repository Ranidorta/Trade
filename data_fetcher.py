import json
import pandas as pd
import requests
from pybit.unified_trading import HTTP

with open('config.json') as f:
    config = json.load(f)

session = HTTP(
    testnet=config.get("testnet", False),
    api_key=config["api_key"],
    api_secret=config["api_secret"]
)

def get_historical_data(start=None, end=None):
    params = {
        "category": config["category"],
        "symbol": config["symbol"],
        "interval": config["interval"]
    }
    if start is not None: params["start"] = start
    if end is not None: params["end"] = end

    res = session.get_kline(**params)
    data = res.get('result', {}).get('list', [])
    df = pd.DataFrame(data, columns=['startTime','open','high','low','close','volume','turnover'])
    df['startTime'] = pd.to_datetime(df['startTime'], unit='ms')
    return df

def get_current_price():
    res = session.get_tickers(category=config["category"], symbol=config["symbol"])
    items = res.get('result', {}).get('list', [])
    if items:
        return float(items[0].get('lastPrice', 0))
    return 0.0

def get_symbols():
    url = "https://api.bybit.com/v5/market/instruments-info"
    params = {"category": "linear", "status": "Trading", "limit": 1000}
    response = requests.get(url, params=params)
    data = response.json()
    symbols = []
    if data.get("retCode") == 0 and "result" in data:
        for item in data["result"].get("list", []):
            if item.get("quoteCoin") == "USDT":
                symbols.append(item["symbol"])
    return symbols