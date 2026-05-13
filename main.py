import os
import telebot
from telebot import types
import requests

# আপনার বটের টোকেন এবং আপডেট করা গ্রুপ লিঙ্ক
TOKEN = os.getenv('BOT_TOKEN')
bot = telebot.TeleBot(TOKEN)
GROUP_LINK = "https://t.me/+EZr3Z1r8Eac0MmE1"

# /start কমান্ড
@bot.message_handler(commands=['start'])
def start(message):
    photo_url = "https://graph.org/file/a6074a3875323868fe06b.jpg"
    markup = types.InlineKeyboardMarkup()
    btn_group = types.InlineKeyboardButton("✨ Join Our Group ✨", url=GROUP_LINK)
    markup.add(btn_group)
    
    caption = (
        "*** 👋 Welcome to BUMBA PVT LTD! ***\n\n"
        "বাইপাস করতে নিচের গ্রুপে জয়েন করুন। 👇"
    )
    
    try:
        bot.send_photo(message.chat.id, photo_url, caption=caption, reply_markup=markup, parse_mode='Markdown')
    except:
        bot.send_message(message.chat.id, caption, reply_markup=markup, parse_mode='Markdown')

# বাইপাস কমান্ড (/b)
@bot.message_handler(commands=['b'])
def bypass(message):
    if message.chat.type == 'private':
        bot.reply_to(message, f"❌ গ্রুপে জয়েন করুন: {GROUP_LINK}")
        return

    args = message.text.split(maxsplit=1)
    if len(args) < 2:
        bot.reply_to(message, "⚠️ লিঙ্ক দিন! যেমন: `/b [link]`")
        return

    url = args[1]
    msg = bot.reply_to(message, "⏳ **BUMBA PVT LTD প্রসেস করছে...**")

    # নতুন এবং শক্তিশালী API ব্যবহার করা হচ্ছে
    try:
        # বিকল্প এপিআই যা আপনার indiaearnx লিঙ্ক সাপোর্ট করতে পারে
        api_url = f"https://adrinolinks.in/api?api=96f86058e17424b953330f576e2704ed92244243&url={url}"
        r = requests.get(api_url, timeout=20)
        data = r.json()

        if data.get("status") == "success":
            res = data.get("shortenedUrl")
            bot.edit_message_text(f"🚀 **BYPASS SUCCESS**\n\n🔓 **Link:** {res}", msg.chat.id, msg.message_id)
        else:
            bot.edit_message_text("❌ এই লিঙ্কটি এই মুহূর্তে বাইপাস করা সম্ভব নয়।", msg.chat.id, msg.message_id)
    except:
        bot.edit_message_text("⚠️ সার্ভার ব্যস্ত। দয়া করে কিছুক্ষণ পর আবার চেষ্টা করুন।", msg.chat.id, msg.message_id)

if __name__ == "__main__":
    bot.infinity_polling()







