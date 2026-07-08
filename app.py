from flask import Flask, request
import threading
import time
from sentiment_engine import run_sentiment_cycle, load_ess_data

app = Flask(__name__)

@app.route("/")
def home():
    return "Sentiment Engine is live!"

@app.route("/sentiment")
def sentiment():
    df = load_ess_data()
    latest = df.iloc[-1]
    return {
        "time": latest["time"].isoformat(),
        "ESS": float(latest["ESS"]),
        "S_short": float(latest["S_short"]),
        "S_long": float(latest["S_long"])
    }

@app.route("/sentiment_feed")
def sentiment_feed():
    df = load_ess_data()
    latest = df.iloc[-1]
    ess = float(latest["ESS"])
    return f"{ess},{ess},{ess},{ess}"

@app.route("/tv-webhook", methods=["POST"])
def tv_webhook():
    data = request.json
    print("TradingView alert received:", data)
    return {"status": "ok"}

def background_loop():
    while True:
        try:
            run_sentiment_cycle()
        except Exception as e:
            print("Error in sentiment cycle:", e)
        time.sleep(60)

threading.Thread(target=background_loop).start()

app.run(host="0.0.0.0", port=10000)
