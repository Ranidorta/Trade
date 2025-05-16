import json
import sqlite3

with open('config.json') as f:
    config = json.load(f)
db_path = config.get("db_path", "signals.db")

def init_db():
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS signals (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT,
            symbol TEXT,
            signal TEXT,
            price REAL,
            size REAL
        )
    """)
    conn.commit()
    conn.close()

def insert_signal(signal):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO signals (timestamp, symbol, signal, price, size)
        VALUES (?, ?, ?, ?, ?)
    """, (signal["time"], signal["symbol"], signal["signal"], signal["price"], signal["size"]))
    conn.commit()
    conn.close()

def get_last_signal(symbol):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("""
        SELECT timestamp, symbol, signal, price FROM signals
        WHERE symbol = ? ORDER BY id DESC LIMIT 1
    """, (symbol,))
    row = cursor.fetchone()
    conn.close()
    if row:
        return {
            "time": row[0],
            "symbol": row[1],
            "signal": row[2],
            "price": row[3]
        }
    return None

init_db()