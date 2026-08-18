import os
import requests
import telebot
from flask import Flask
from threading import Thread

# 1. Flask serveri (Render portni aniqlashi uchun)
app = Flask('')

@app.route('/')
def home():
    return "Bot muvaffaqiyatli ishlamoqda!"

def run():
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)

# Flask'ni orqa fonda ishga tushirish
Thread(target=run).start()

# 2. Telegram Bot sozlamalari
TOKEN = "8772035660:AAEPI673hlAxluh81JGJVseDQafwFNQYLw0"
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, "Salom! Valyuta botiga xush kelibsiz. Valyuta kurslarini bilish uchun /kurs buyrug'ini yuboring.")

@bot.message_handler(commands=['kurs'])
def get_rate(message):
    try:
        response = requests.get("https://cbu.uz/uz/arkhiv-kursov-valyut/json/").json()
        usd = response[0]['Rate']
        eur = response[1]['Rate']
        rub = response[2]['Rate']
        
        text = f"<b>Bugungi valyuta kurslari:</b>\n\n" \
               f"1 USD = {usd} so'm\n" \
               f"1 EUR = {eur} so'm\n" \
               f"1 RUB = {rub} so'm"
               
        bot.send_message(message.chat.id, text, parse_mode="HTML")
    except Exception as e:
        bot.reply_to(message, "Valyuta kurslarini olishda xatolik yuz berdi.")

# 3. Botni ishga tushirish (KODNING ENG OXIRIDA BO'LISHI SHART!)
bot.infinity_polling()