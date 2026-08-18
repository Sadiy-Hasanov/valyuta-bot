import os
import requests
import telebot
from flask import Flask
from threading import Thread

app = Flask('')

@app.route('/')
def home():
    return "Bot muvaffaqiyatli ishlamoqda!"

def run():
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)

Thread(target=run).start()

TOKEN = "8772035660:AAEPI673hlAxluh81JGJVseDQafwFNQYLw0"
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, "Salom! Summani so'mda kiriting (masalan: 30000 yoki 100000), men uni valyutalarga hisoblab beraman!")

# Har qanday kiritilgan matn va sonlarni hisoblash funksiyasi
@bot.message_handler(func=lambda message: True)
def convert_currency(message):
    try:
        som = float(message.text.replace(" ", ""))
        response = requests.get("https://cbu.uz/uz/arkhiv-kursov-valyut/json/").json()
        
        usd_rate = float(response[0]['Rate'])
        eur_rate = float(response[1]['Rate'])
        rub_rate = float(response[2]['Rate'])
        
        usd_val = round(som / usd_rate, 2)
        eur_val = round(som / eur_rate, 2)
        rub_val = round(som / rub_rate, 2)
        
        text = f"💱 <b>{som:,.0f} so'm</b> quyidagiga teng:\n\n" \
               f"🇺🇸 USD: {usd_val} dollar\n" \
               f"🇪🇺 EUR: {eur_val} yevro\n" \
               f"🇷🇺 RUB: {rub_val} rubl"
               
        bot.send_message(message.chat.id, text, parse_mode="HTML")
    except ValueError:
        bot.reply_to(message, "Iltimos, faqat raqam kiriting (masalan: 50000).")
    except Exception as e:
        bot.reply_to(message, "Valyuta kursini olishda xatolik yuz berdi.")

bot.infinity_polling()