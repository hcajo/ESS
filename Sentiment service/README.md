# ESS
# Sentiment Engine (Render Deployment)

## 1. Push this folder to GitHub

## 2. On Render:
- Click "New → Web Service"
- Select your GitHub repo
- Render will detect render.yaml automatically
- Click "Deploy"

## 3. Continuous Runtime
The service runs app.py continuously.
Sentiment cycles run every 60 seconds.

## 4. TradingView Webhook (optional)
Send alerts to:
https://your-service.onrender.com/tv-webhook
