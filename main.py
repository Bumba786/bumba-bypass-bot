import os
import telebot
import requests
import time
from telebot import types

# --- Configuration ---
TOKEN = os.getenv('BOT_TOKEN')
bot = telebot.TeleBot(TOKEN)
GROUP_LINK = "https://t.me/+EZr3ZIr8Eac0MmE1"

# আদ্রি লিঙ্কের জন্য একটি ব্যাকআপ API ডোমেইন (যা অনেক সময় সচল থাকে)
ADRINELINKS_API_URL = "https://adrinelinks.in/api"
API_KEY = os.getenv('API_KEY', '96f86058e17424b89311059f31a19616e0339d37')

def get_bypass_result(url):
    """একাধিক মেথড ব্যবহার করে বাইপাস করার চেষ্টা করবে"""
    
    # মেথড ১: মাল্টি-বাইপাস পাবলিক API (সবচেয়ে শক্তিশালী)
    try:
        r = requests.get(f"https://api.bypass.vip/bypass?url={url}", timeout=15)
        data = r.json()
        if data.get("status") == "success":
            return data.get("destination")
    except:
        pass

    # মেথড ২: Adrinelinks Fallback
    try:
        params = {'api': API_KEY, 'url': url}
        r = requests.get(ADRINELINKS_API_URL, params=params, timeout=15)
        data = r.json()
        if data.get("status") == "success":
            return data.get("shortenedUrl")
    except:
        pass

    return None

@bot.message_handler(commands=['start'])
def start(message):
    photo_url = "https://graph.org/file/a8074a3875323868fe08b.jpg"
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("📢 Join Our Group 📢", url=GROUP_LINK))
    
    caption = (
        "✨ **Welcome to BUMBA PVT LTD!** ✨\n\n"
        "লিঙ্ক বাইপাস করতে নিচের ফরম্যাটটি ব্যবহার করুন:\n"
        "🔗 `/b https://link.com`"
    )
    
    try:
        bot.send_photo(message.chat.id, photo_url, caption=caption, reply_markup=markup, parse_mode="Markdown")
    except:
        bot.send_message(message.chat.id, caption, reply_markup=markup, parse_mode="Markdown")

@bot.message_handler(commands=['b'])
def bypass(message):
    if message.chat.type == "private":
        # প্রাইভেট চ্যাটে রেস্ট্রিকশন থাকলে এখানে কোড যোগ করা যায়
        pass

    args = message.text.split(maxsplit=1)
    if len(args) < 2:
        bot.reply_to(message, "⚠️ **লিঙ্ক দিন!**\nউদাহরণ: `/b https://indiaearnx.com/xxx`", parse_mode="Markdown")
        return

    url = args[1].strip()
    
    # সুন্দর প্রগ্রেস বার ডিজাইন
    sent_msg = bot.reply_to(message, "⏳ **Bypassing :- 10%**\n`[#---------]`", parse_mode="Markdown")
    time.sleep(0.5)
    bot.edit_message_text("⏳ **Bypassing :- 60%**\n`[######---]`", sent_msg.chat.id, sent_msg.message_id, parse_mode="Markdown")
    
    # রেজাল্ট খোঁজা
    result = get_bypass_result(url)
    
    if result:
        time.sleep(0.3)
        bot.edit_message_text("⏳ **Bypassing :- 100%**\n`[##########]`", sent_msg.chat.id, sent_msg.message_id, parse_mode="Markdown")
        
        final_text = (
            "✅ **Bypass Successful!**\n\n"
            f"🔗 **Original Link:** `{url}`\n\n"
            f"🔓 **Bypassed Link:** {result}\n\n"
            "✨ *Powered by Bumba Pvt Ltd*"
        )
        bot.edit_message_text(final_text, sent_msg.chat.id, sent_msg.message_id, parse_mode="Markdown", disable_web_page_preview=True)
    else:
        error_text = (
            "❌ **Failed!!**\n\n"
            "এই লিঙ্কটি বর্তমানে বাইপাস করা সম্ভব হচ্ছে না।\n"
            "সার্ভার ডাউন থাকতে পারে। পরে আবার চেষ্টা করুন।"
        )
        bot.edit_message_text(error_text, sent_msg.chat.id, sent_msg.message_id, parse_mode="Markdown")

if __name__ == "__main__":
    print("Bot is running...")
    bot.infinity_polling()













