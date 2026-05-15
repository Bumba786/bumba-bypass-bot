import os
import telebot
import requests
import re
import time
from telebot import types

# --- কনফিগারেশন ---
TOKEN = os.getenv('BOT_TOKEN')
bot = telebot.TeleBot(TOKEN)

MY_API_KEY = "adec84f7928c09e3aa63531c5be3b240d12e25c6"
GROUP_LINK = "https://t.me/+EZr3ZIr8Eac0MmE1"
BRAND = "👑 BUMBA PVT LTD 👑"

# --- বাইপাস করার বিশেষ লজিক ---
def attempt_bypass(url):
    client = requests.Session()
    # হাই-লেভেল হেডার যাতে সাইট মনে করে এটা আসল ব্রাউজার
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
        'Referer': 'https://google.com/'
    }
    try:
        # ১. সরাসরি স্ক্র্যাপিং (Indiaearnx এর সিকিউরিটি ভাঙার চেষ্টা)
        response = client.get(url, headers=headers, timeout=12)
        # অনেক সময় লিঙ্কের গন্তব্য জাভাস্ক্রিপ্ট ভেরিয়েবল 'url' বা 'link' এ থাকে
        found = re.findall(r"var\s+(?:url|link)\s+=\s+'([^']+)'", response.text)
        if found:
            return found[0]

        # ২. ব্যাকআপ হিসেবে আপনার এপিআই ব্যবহার
        api_url = f"https://egolinks.site/api?api={MY_API_KEY}&url={url}"
        api_res = requests.get(api_url, timeout=10).json()
        if api_res.get("status") == "success":
            return api_res.get("shortened_url")
            
    except Exception:
        pass
    return None

# --- স্টার্ট মেসেজ ডিজাইন ---
@bot.message_handler(commands=['start'])
def start(message):
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("📢 JOIN OUR GROUP ↗️", url=GROUP_LINK))
    
    welcome_text = (
        f"┌──────────────『 {BRAND} 』──────────────┐\n\n"
        f"👋 **হ্যালো ওস্তাদ, {message.from_user.first_name}!**\n\n"
        "আমি আপনার অ্যাডভান্সড বাইপাস টুল। যেকোনো শর্টলিঙ্ক\n"
        "থেকে আসল লিঙ্ক বের করতে জাস্ট লিঙ্কটি পাঠান।\n\n"
        "🚀 **কমান্ড:** `/b [আপনার লিঙ্ক]`\n\n"
        "└────────────────────────────────────────┘"
    )
    bot.send_message(message.chat.id, welcome_text, reply_markup=markup, parse_mode="Markdown")

# --- বাইপাস হ্যান্ডলার (ডিজাইন সহ) ---
@bot.message_handler(commands=['b'])
def handle_b(message):
    args = message.text.split(maxsplit=1)
    if len(args) < 2:
        bot.reply_to(message, "⚠️ **ওস্তাদ, লিঙ্ক দিতে ভুলে গেছেন!**", parse_mode="Markdown")
        return

    url = args[1].strip()
    status = bot.reply_to(message, "🔍 **লিঙ্ক অ্যানালাইজ করা হচ্ছে...**\n`[▒▒▒▒▒▒▒▒▒▒] 0%`", parse_mode="Markdown")
    
    # লোডিং অ্যানিমেশন (দেখতে সুন্দর লাগে)
    time.sleep(1)
    bot.edit_message_text("⚙️ **সিকিউরিটি ভাঙার চেষ্টা করছি...**\n`[████▒▒▒▒▒▒] 45%`", status.chat.id, status.message_id, parse_mode="Markdown")
    
    result = attempt_bypass(url)
    
    if result:
        # সাকসেস ডিজাইন
        res_markup = types.InlineKeyboardMarkup()
        res_markup.add(types.InlineKeyboardButton("🔗 ওপেন লিঙ্ক 🔗", url=result))
        res_markup.add(types.InlineKeyboardButton("📢 জয়েন গ্রুপ 📢", url=GROUP_LINK))
        
        final_msg = (
            f"┏━━━━━━『 **BYPASS SUCCESS** 』━━━━━━┓\n\n"
            f"📥 **অরিজিনাল:** `{url}`\n\n"
            f"📤 **রেজাল্ট:** `{result}`\n\n"
            "━━━━━━━━━━━━━━━━━━━━━━\n"
            f"👑 **Powered by {BRAND}**\n"
            f"┗━━━━━━━━━━━━━━━━━━━━━━┛"
        )
        bot.edit_message_text(final_msg, status.chat.id, status.message_id, reply_markup=res_markup, parse_mode="Markdown", disable_web_page_preview=True)
    else:
        # এরর ডিজাইন
        bot.edit_message_text(
            f"❌ **বাইপাস ব্যর্থ হয়েছে!**\n\n"
            f"এই লিঙ্কের সিকিউরিটি অনেক হাই। আমাদের গ্রুপে জানান:\n{GROUP_LINK}", 
            status.chat.id, status.message_id, disable_web_page_preview=True
        )

if __name__ == "__main__":
    bot.infinity_polling()


