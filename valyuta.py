import telebot
import requests

# BotFather'dan olgan tokenni shu yerga qo'ying
TOKEN = "8772035660:AAEPI673hlAxluh81JGJVseDQafwFNQYLw0"
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def start_message(message):
    bot.reply_to(message, "Salom! So'm miqdorini kiriting (masalan: 300000), men uni valyutalarga hisoblab beraman.")

@bot.message_handler(func=lambda message: message.text.isdigit())
def convert_money(message):
    try:
        som = float(message.text)
        url = "https://cbu.uz/uz/arkhiv-kursov-valyut/json/"
        response = requests.get(url).json()

        usd_rate = float(next(item for item in response if item['Ccy'] == 'USD')['Rate'])
        eur_rate = float(next(item for item in response if item['Ccy'] == 'EUR')['Rate'])
        rub_rate = float(next(item for item in response if item['Ccy'] == 'RUB')['Rate'])

        usd = round(som / usd_rate, 2)
        eur = round(som / eur_rate, 2)
        rub = round(som / rub_rate, 2)

        text = (
            f"💱 <b>{som:,.0f} so'm</b> quyidagiga teng:\n\n"
            f"🇺🇸 USD: {usd} dollar\n"
            f"🇪🇺 EUR: {eur} yevro\n"
            f"🇷🇺 RUB: {rub} rubl"
        )
        bot.send_message(message.chat.id, text, parse_mode='HTML')
    except Exception:
        bot.send_message(message.chat.id, "Xatolik yuz berdi. Iltimos qaytadan urinib ko'ring.")

bot.polling(none_stop=True)