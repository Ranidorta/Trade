import json
from data_fetcher import get_current_price

with open('config.json') as f:
    config = json.load(f)

def calculate_position_size():
    balance = config.get("account_balance", 0)
    risk_pct = config.get("risk_per_trade", 0)
    price = get_current_price()
    max_risk = balance * risk_pct
    stop_loss_val = price * 0.01
    if stop_loss_val <= 0:
        return 0
    return max_risk / stop_loss_val

def manage_risk(signal):
    if signal is None:
        return None
    size = calculate_position_size()
    signal["size"] = size
    return signal