import telebot
import requests
import os

# এখানে টোকেন সরাসরি না লিখে আমরা Railway থেকে নেব
TOKEN = os.getenv('BOT_TOKEN')
API = "https://web-production-6701d.up.railway.app/bypass"

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "👋 Welcome to BUMBA PRIVATE BOT!\n\nযেকোনো লিঙ্ক পাঠান।")

@bot.message_handler(func=lambda m: True)
def bypass_link(message):
    url = message.text.strip()
    bot.reply_to(message, "⏳ BUMBA প্রসেস করছে...")
    try:
        r = requests.post(API, json={"url": url})
        bot.send_message(message.chat.id, f"✅ Result:\n\n{r.text}")
    except:
        bot.send_message(message.chat.id, "❌ সমস্যা হয়েছে।")

bot.infinity_polling()

