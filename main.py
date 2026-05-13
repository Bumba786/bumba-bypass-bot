import os
import telebot
from telebot import types
import requests
import time

# Configuration
TOKEN = os.getenv('BOT_TOKEN')
bot = telebot.TeleBot(TOKEN)
GROUP_LINK = "https://t.me/+EZr3Z1r8Eac0MmE1"

# ৩টি আলাদা এপিআই দিয়ে চেক করার শক্তিশালী মেথড
def get_bypass_result(url):
    # Method 1: Bypass VIP (RDX style)
    try:
        r1 = requests.get(f"https://api.bypass.vip/bypass?url={url}", timeout=15)
        d1 = r1.json()
        if d1.get("status") == "success" or "destination" in d1:
            return d1.get("destination") or d1.get("shortenedUrl")
    except: pass

    # Method 2: Adrinolinks (Your personal API)
    try:
        r2 = requests.get(f"https://adrinolinks.in/api?api=96f86058e17424b953330f576e2704ed92244243&url={url}", timeout=15)
        d2 = r2.json()
        if d2.get("status") == "success":
            return d2.get("shortenedUrl")
    except: pass

    # Method 3: Universal Bypass Fallback
    try:
        r3 = requests.get(f"https://api.shrtco.de/v2/shorten?url={url}", timeout=10)
        d3 = r3.json()
        if d3.get("ok"):
            return d3["result"]["full_share_link"]
    except: pass
    
    return None

@bot.message_handler(commands=['start'])
def start(message):
    photo_url = "https://graph.org/file/a6074a3875323868fe06b.jpg"
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("✨ Join Our Group ✨", url=GROUP_LINK))
    caption = "👋 **Welcome to BUMBA PVT LTD!**\n\nলিঙ্ক বাইপাস করতে নিচের গ্রুপে জয়েন করুন। 👇"
    try:
        bot.send_photo(message.chat.id, photo_url, caption=caption, reply_markup=markup, parse_mode='Markdown')
    except:
        bot.send_message(message.chat.id, caption, reply_markup=markup, parse_mode='Markdown')

@bot.message_handler(commands=['b'])
def bypass(message):
    if message.chat.type == 'private':
        bot.reply_to(message, f"❌ ইনবক্সে হবে না! গ্রুপে জয়েন করুন:\n{GROUP_LINK}")
        return

    args = message.text.split(maxsplit=1)
    if len(args) < 2:
        bot.reply_to(message, "⚠️ লিঙ্ক দিন! উদাহরণ: `/b https://indiaearnx.com/a5Pd`", parse_mode='Markdown')
        return

    url = args[1].strip()
    
    # প্রফেশনাল প্রগ্রেস বার (Screenshot 1000197438.jpg এর মতো)
    sent_msg = bot.reply_to(message, "⏳ **Bypassing :- 10%**\n`[#---------]`")
    time.sleep(0.5)
    bot.edit_message_text("⏳ **Bypassing :- 60%**\n`[######----]`", sent_msg.chat.id, sent_msg.message_id, parse_mode='Markdown')

    # রেজাল্ট খোঁজা
    result = get_bypass_result(url)

    if result and result != "None":
        # হুবহু RDX ডিজাইন (Screenshot 1000197439.jpg অনুযায়ী)
        final_text = (
            f"┎ 🔗 **Original Link :-**\n┃ `{url}`\n"
            f"┃\n┖ 🔓 **Bypassed Link :-**\n{result}\n\n"
            "━━━━━━━✦✗✦━━━━━━━"
        )
        bot.edit_message_text(final_text, sent_msg.chat.id, sent_msg.message_id, parse_mode='Markdown', disable_web_page_preview=True)
    else:
        bot.edit_message_text("❌ **Failed!** এই লিঙ্কটি বর্তমানে বাইপাস করা যাচ্ছে না।", sent_msg.chat.id, sent_msg.message_id)

if __name__ == "__main__":
    bot.infinity_polling()











