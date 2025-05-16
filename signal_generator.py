import json
from datetime import datetime
from data_fetcher import get_historical_data, get_current_price
from utils.indicators import SMA, RSI

with open('config.json') as f:
    config = json.load(f)

def generate_signal(symbol):
    df = get_historical_data()
    if df.empty:
        return None

    close = df['close'].astype(float)
    sma_short = SMA(close, config["moving_avg_short"]).iloc[-1]
    sma_long = SMA(close, config["moving_avg_long"]).iloc[-1]
    rsi = RSI(close, config["rsi_period"]).iloc[-1]

    if sma_short > sma_long:
        action = "buy"
    elif sma_short < sma_long:
        action = "sell"
    else:
        action = "hold"

    price = get_current_price()
    return {
        "symbol": symbol,
        "signal": action,
        "price": price,
        "time": datetime.utcnow().isoformat()
    }