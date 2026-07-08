import time
from sentiment_engine import run_sentiment_cycle
from flask import Flask, request
import threading

# Optional: enable TradingView webhook listener
ENABLE_WEBHOOK = True

app = Flask(__name__)

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
        time.sleep(60)  # run every minute

if ENABLE_WEBHOOK:
    threading.Thread(target=background_loop).start()
    app.run(host="0.0.0.0", port=10000)
else:
    background_loop()
