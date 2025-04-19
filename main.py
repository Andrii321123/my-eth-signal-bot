import os
import time
import requests
from telegram import Bot

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")
bot = Bot(token=BOT_TOKEN)

# Встановлюємо пороги ціни
PRICE_UPPER = 3400   # Тейк-профіт
PRICE_LOWER = 3200   # Стоп-лосс або вигідний вхід

def get_eth_price():
    url = "https://api.bybit.com/v5/market/tickers?category=linear"
    response = requests.get(url)
    data = response.json()

    for ticker in data["result"]["list"]:
        if ticker["symbol"] == "ETHUSDT":
            return float(ticker["lastPrice"])
    return None

last_signal = None  # Щоб не дублювати повідомлення

while True:
    try:
        price = get_eth_price()
        if price:
            print(f"ETH price: {price}")

            if price > PRICE_UPPER and last_signal != "long":
                bot.send_message(chat_id=CHAT_ID, text=f"🚀 ETH пробив {PRICE_UPPER}$ — розглянь ЛОНГ!")
                last_signal = "long"

            elif price < PRICE_LOWER and last_signal != "short":
                bot.send_message(chat_id=CHAT_ID, text=f"📉 ETH впав нижче {PRICE_LOWER}$ — розглянь ШОРТ!")
                last_signal = "short"
        else:
            print("Не вдалося отримати ціну ETH")

    except Exception as e:
        print("⚠️ Помилка:", e)

    time.sleep(60)  # Перевіряє раз на хвилину
