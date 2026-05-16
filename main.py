import os
import telebot
import requests
import re
import time
from telebot import types

# --- কনফিগারেশন ---
TOKEN = os.getenv('BOT_TOKEN') # রেলওয়ে বা ভিপিএস-এ আপনার বটের টোকেন
bot = telebot.TeleBot(TOKEN)

# আপনার এপিআই এবং গ্রুপের তথ্য
RAILWAY_API_URL = "https://web-production-6701d.up.railway.app/bypass"
EGOLINKS_API_KEY = "adec84f7928c09e3aa63531c5be3b240d12e25c6"
GROUP_LINK = "https://t.me/+EZr3ZIr8Eac0MmE1"
BRAND = "👑 BUMBA PVT LTD 👑"

# --- স্মার্ট মাল্টি-এপিআই ইঞ্জিন (অটো ব্যাকআপ সিস্টেম) ---
def smart_bypass(url):
    client = requests.Session()
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36'
    }

    # 🚀 ১ নম্বর চেষ্টা: আপনার রেলওয়ে এপিআই
    try:
        params = {'url': url}
        response = requests.get(RAILWAY_API_URL, params=params, timeout=8)
        if response.status_code == 200:
            data = response.json()
            for key in ["bypassed_url", "url", "link", "bypassed"]:
                if key in data and data[key]:
                    return data[key]
    except Exception:
        pass

    # 🔄 ২ নম্বর চেষ্টা (ব্যাকআপ): আপনার Egolinks API
    try:
        api_url = f"https://egolinks.site/api?api={EGOLINKS_API_KEY}&url={url}"
        api_res = requests.get(api_url, timeout=8).json()
        if api_res.get("status") == "success":
            return api_res.get("shortened_url")
    except Exception:
        pass

    # 🛠 ৩ নম্বর চেষ্টা (শেষ ভরসা): সোর্স কোড স্ক্র্যাপিং (Shortxlinks এর জন্য)
    try:
        res = client.get(url, headers=headers, timeout=8)
        found = re.findall(r"var\s+(?:url|link|targetUrl)\s+=\s+'([^']+)'", res.text)
        if found:
            return found[0]
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

# --- বাইপাস হ্যান্ডলার (প্রিমিয়াম বক্স স্টাইল) ---
@bot.message_handler(commands=['b'])
def handle_b(message):
    args = message.text.split(maxsplit=1)
    if len(args) < 2:
        bot.reply_to(message, "⚠️ **ওস্তাদ, লিঙ্ক দিতে ভুলে গেছেন!**\nসঠি নিয়ম: `/b https://link.com`", parse_mode="Markdown")
        return

    url = args[1].strip()
    status = bot.reply_to(message, "🔍 **লিঙ্ক অ্যানালাইজ করা হচ্ছে...**\n`[▒▒▒▒▒▒▒▒▒▒] 0%`", parse_mode="Markdown")
    
    time.sleep(0.5)
    bot.edit_message_text("⚙️ **স্মার্ট বাইপাস ইঞ্জিন চালু হচ্ছে...**\n`[████▒▒▒▒▒▒] 45%`", status.chat.id, status.message_id, parse_mode="Markdown")
    
    # ব্যাকআপ ইঞ্জিন রান করা হলো
    result = smart_bypass(url)
    
    if result:
        bot.edit_message_text("✅ **বাইপাস সফল!**\n`[██████████] 100%`", status.chat.id, status.message_id, parse_mode="Markdown")
        time.sleep(0.3)
        
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
        error_markup = types.InlineKeyboardMarkup()
        error_markup.add(types.InlineKeyboardButton("🆘 রিপোর্ট করুন", url=GROUP_LINK))
        
        error_msg = (
            "❌ **বাইপাস ব্যর্থ হয়েছে!**\n\n"
            "সবগুলো বাইপাস মেথড চেষ্টা করা হয়েছে, কিন্তু লিঙ্কটি ভাঙা যায়নি।\n\n"
            f"📢 **সহযোগিতার জন্য গ্রুপে জানান:**\n{GROUP_LINK}"
        )
        bot.edit_message_text(error_msg, status.chat.id, status.message_id, reply_markup=error_markup, parse_mode="Markdown", disable_web_page_preview=True)

if __name__ == "__main__":
    bot.infinity_polling()



