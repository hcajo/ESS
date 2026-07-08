import pandas as pd
import requests
from datetime import datetime

from config import WEBHOOK_URL, ONE_WEEK_DAYS, THREE_MONTH_DAYS
from utils.logger import log

def load_ess_data():
    df = pd.read_csv("ess_data.csv", parse_dates=["time"])
    df = df[df["ESS"] != 50].sort_values("time")
    return df

def compute_sentiment(df):
    df = df.set_index("time").resample("1T").last().ffill()

    one_week_window = ONE_WEEK_DAYS * 24 * 60
    three_month_window = THREE_MONTH_DAYS * 24 * 60

    df["S_short"] = df["ESS"].rolling(window=one_week_window, min_periods=1).mean()
    df["S_long"] = df["ESS"].rolling(window=three_month_window, min_periods=1).mean()

    return df

def detect_crossovers(df):
    signals = []
    prev_row = None

    for ts, row in df.iterrows():
        if prev_row is None:
            prev_row = row
            continue

        prev_diff = prev_row["S_short"] - prev_row["S_long"]
        curr_diff = row["S_short"] - row["S_long"]

        if prev_diff <= 0 and curr_diff > 0:
            signals.append({
                "time": ts,
                "signal": "BULLISH",
                "S_short": row["S_short"],
                "S_long": row["S_long"]
            })

        if prev_diff >= 0 and curr_diff < 0:
            signals.append({
                "time": ts,
                "signal": "BEARISH",
                "S_short": row["S_short"],
                "S_long": row["S_long"]
            })

        prev_row = row

    return signals

def send_webhook(signal):
    payload = {
        "time": signal["time"].isoformat(),
        "signal": signal["signal"],
        "S_short": signal["S_short"],
        "S_long": signal["S_long"],
        "reason": "1-week vs 3-month sentiment crossover"
    }

    try:
        r = requests.post(WEBHOOK_URL, json=payload, timeout=5)
        log(f"Webhook sent ({signal['signal']}): {r.status_code}")
    except Exception as e:
        log(f"Webhook error: {e}")

def run_sentiment_cycle():
    log("Starting sentiment cycle...")
    df = load_ess_data()
    df = compute_sentiment(df)
    signals = detect_crossovers(df)

    for sig in signals:
        send_webhook(sig)

    log("Cycle complete.")
