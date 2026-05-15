import os
import telebot
import requests
import re
import time
from telebot import types

# --- সেটিংস ও কনফিগারেশন ---
TOKEN = os.getenv('BOT_TOKEN') # আপনার বট টোকেন (রেলওয়েতে ভেরিয়েবল হিসেবে দেবেন)
bot = telebot.TeleBot(TOKEN)

# আপনার তথ্য
MY_API_KEY = "adec84f7928c09e3aa63531c5be3b240d12e25c6"
GROUP_LINK = "https://t.me/+EZr3ZIr8Eac0MmE1"
BRAND = "👑 BUMBA PVT LTD 👑"

# --- বাইপাস লজিক (The Engine) ---
def get_bypass(url):
    client = requests.Session()
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Referer': 'https://google.com/'
    }
    try:
        # ১. স্ক্র্যাপিং করার চেষ্টা (Indiaearnx বা ডাইনামিক সাইটের জন্য)
        res = client.get(url, headers=headers, timeout=10)
        found = re.findall(r"var\s+url\s+=\s+'([^']+)'", res.text)
        if found:
            return found[0]
        
        # ২. ব্যাকআপ হিসেবে আপনার Egolinks API
        api_url = f"https://egolinks.site/api?api={MY_API_KEY}&url={url}"
        api_res = requests.get(api_url, timeout=10).json()
        if api_res.get("status") == "success":
            return api_res.get("shortened_url")
    except:
        pass
    return None

# --- স্টার্ট কমান্ড (ডিজাইন করা মেসেজ) ---
@bot.message_handler(commands=['start'])
def start(message):
    markup = types.InlineKeyboardMarkup()
    markup.row(types.InlineKeyboardButton("📢 OFFICIAL GROUP", url=GROUP_LINK))
    markup.row(
        types.InlineKeyboardButton("🛠 SUPPORT", url=GROUP_LINK),
        types.InlineKeyboardButton("👑 OWNER", url="https://t.me/your_username")
    )
    
    welcome_text = (
        f"┏━━━━━━『 **{BRAND}** 』━━━━━━┓\n\n"
        f"👋 **স্বাগতম ওস্তাদ, {message.from_user.first_name}!**\n\n"
        "আমি আপনার পার্সোনাল বাইপাস অ্যাসিস্ট্যান্ট।\n"
        "যেকোনো লিঙ্ক দিন, আমি অরিজিনাল লিঙ্ক বের করে দেব।\n\n"
        "🚀 **ব্যবহার:** `/b [লিঙ্ক]` লিখে পাঠান।\n\n"
        "┗━━━━━━━━━━━━━━━━━━━━━━┛"
    )
    bot.send_message(message.chat.id, welcome_text, reply_markup=markup, parse_mode="Markdown")

# --- বাইপাস কমান্ড (প্রো ডিজাইনের সাথে) ---
@bot.message_handler(commands=['b'])
def handle_b(message):
    args = message.text.split(maxsplit=1)
    if len(args) < 2:
        bot.reply_to(message, "⚠️ **লিঙ্ক দিতে ভুল করেছেন!**\nসঠিক নিয়ম: `/b https://google.com`", parse_mode="Markdown")
        return

    url = args[1].strip()
    
    # স্টাইলিশ প্রগ্রেস বার ডিজাইন
    status = bot.reply_to(message, "⚙️ **অ্যানালাইজ করা হচ্ছে...**\n`[▒▒▒▒▒▒▒▒▒▒] 0%`", parse_mode="Markdown")
    time.sleep(1) # দেখার সৌন্দর্যের জন্য সাময়িক বিরতি
    
    bot.edit_message_text("⚙️ **সিকিউরিটি চেক হচ্ছে...**\n`[████▒▒▒▒▒▒] 45%`", status.chat.id, status.message_id, parse_mode="Markdown")
    
    result = get_bypass(url)
    
    if result:
        bot.edit_message_text("✅ **বাইপাস সফল!**\n`[██████████] 100%`", status.chat.id, status.message_id, parse_mode="Markdown")
        time.sleep(0.5)
        
        # ফাইনাল রেজাল্ট কার্ড ডিজাইন
        res_markup = types.InlineKeyboardMarkup()
        res_markup.add(types.InlineKeyboardButton("🔗 ওপেন লিঙ্ক 🔗", url=result))
        res_markup.add(types.InlineKeyboardButton("📢 জয়েন গ্রুপ 📢", url=GROUP_LINK))
        
        final_msg = (
            f"┏━━━━『 **BYPASS SUCCESS** 』━━━━┓\n\n"
            f"📥 **অরিজিনাল:** `{url}`\n\n"
            f"📤 **রেজাল্ট:** {result}\n\n"
            f"👤 **রিকোয়েস্ট বাই:** {message.from_user.first_name}\n"
            "━━━━━━━━━━━━━━━━━━━━━\n"
            f"👑 **Powered by {BRAND}**\n"
            f"┗━━━━━━━━━━━━━━━━━━━━━┛"
        )
        bot.edit_message_text(final_msg, status.chat.id, status.message_id, reply_markup=res_markup, parse_mode="Markdown", disable_web_page_preview=True)
    else:
        error_msg = (
            "❌ **বাইপাস ব্যর্থ হয়েছে!**\n\n"
            "এই লিঙ্কের সিকিউরিটি বর্তমানে অনেক শক্তিশালী।\n"
            "আমরা এটি চেক করছি।\n\n"
            f"📢 **গ্রুপে জানান:** {GROUP_LINK}"
        )
        bot.edit_message_text(error_msg, status.chat.id, status.message_id, parse_mode="Markdown", disable_web_page_preview=True)

# --- বট স্টার্ট ---
if __name__ == "__main__":
    print("Bot is starting...")
    bot.infinity_polling()

