import os
import requests
import time
from telegram import Bot

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")
bot = Bot(token=BOT_TOKEN)

def get_funding_rate():
    url = "https://api.bybit.com/v5/market/funding/history"
    params = {
        "symbol": "ETHUSDT",
        "limit": 1
    }
    response = requests.get(url, params=params)
    data = response.json()
    rate = float(data["result"]["list"][0]["fundingRate"])
    return rate * 100

def send_signal(message):
    bot.send_message(chat_id=CHAT_ID, text=message)

def main():
    while True:
        try:
            rate = get_funding_rate()
            if rate < -0.01:
                send_signal(f"💥 Funding Rate ETH: {rate:.4f}% — МОЖЛИВИЙ ЛОНГ")
            elif rate > 0.01:
                send_signal(f"🔻 Funding Rate ETH: {rate:.4f}% — МОЖЛИВИЙ ШОРТ")
        except Exception as e:
            print(f"Error: {e}")
        time.sleep(60)

if __name__ == "__main__":
    main()