from database import get_last_signal

def validate_signal(signal):
    if signal is None:
        return None
    last = get_last_signal(signal["symbol"])
    if last and last.get("signal") == signal.get("signal"):
        return None
    return signal