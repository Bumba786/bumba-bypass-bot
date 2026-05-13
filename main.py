import os
import telebot
from telebot import types
import requests
import time

TOKEN = os.getenv('BOT_TOKEN')
bot = telebot.TeleBot(TOKEN)
GROUP_LINK = "https://t.me/+EZr3Z1r8Eac0MmE1"

@bot.message_handler(commands=['start'])
def start(message):
    photo_url = "https://graph.org/file/a6074a3875323868fe06b.jpg"
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("✨ Join Our Group ✨", url=GROUP_LINK))
    caption = "👋 **Welcome to BUMBA PVT LTD!**\n\nবাইপাস করতে আমাদের গ্রুপে জয়েন করুন। 👇"
    try:
        bot.send_photo(message.chat.id, photo_url, caption=caption, reply_markup=markup, parse_mode='Markdown')
    except:
        bot.send_message(message.chat.id, caption, reply_markup=markup, parse_mode='Markdown')

@bot.message_handler(commands=['b'])
def bypass(message):
    if message.chat.type == 'private':
        bot.reply_to(message, f"❌ গ্রুপে জয়েন করুন: {GROUP_LINK}")
        return

    args = message.text.split(maxsplit=1)
    if len(args) < 2:
        bot.reply_to(message, "⚠️ লিঙ্ক দিন! উদাহরণ: `/b https://indiaearnx.com/a5Pd`", parse_mode='Markdown')
        return

    url = args[1]
    
    # RDX স্টাইল প্রগ্রেস বার (স্ক্রিনশট 1000197436_2.jpg এর মতো)
    sent_msg = bot.reply_to(message, "⏳ **Bypassing :- 0%**\n`[----------]`")
    time.sleep(1)
    bot.edit_message_text(f"⏳ **Bypassing :- 40%**\n`[####------]`", sent_msg.chat.id, sent_msg.message_id, parse_mode='Markdown')
    time.sleep(1)
    bot.edit_message_text(f"⏳ **Bypassing :- 80%**\n`[########--]`", sent_msg.chat.id, sent_msg.message_id, parse_mode='Markdown')

    try:
        # প্রফেশনাল এপিআই ব্যবহার
        api_url = f"https://adrinolinks.in/api?api=96f86058e17424b953330f576e2704ed92244243&url={url}"
        r = requests.get(api_url, timeout=20)
        data = r.json()

        if data.get("status") == "success":
            res = data.get("shortenedUrl")
            final_text = (
                "✅ **BYPASS SUCCESS**\n"
                "━━━━━━━━━━━━━━━\n"
                f"🔗 **Original:** `{url}`\n"
                f"🔓 **Bypassed:** `{res}`\n"
                "━━━━━━━━━━━━━━━\n"
                "👤 **Requested By:** " + message.from_user.first_name
            )
            bot.edit_message_text(final_text, sent_msg.chat.id, sent_msg.message_id, parse_mode='Markdown')
        else:
            bot.edit_message_text("❌ **লিঙ্কটি বাইপাস করা সম্ভব হয়নি!** আমাদের অন্য এপিআই ট্রাই করুন।", sent_msg.chat.id, sent_msg.message_id)
    except:
        bot.edit_message_text("⚠️ **সার্ভার এরর!** পরে চেষ্টা করুন।", sent_msg.chat.id, sent_msg.message_id)

if __name__ == "__main__":
    bot.infinity_polling()









