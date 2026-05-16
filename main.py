import os
import telebot
import requests
import time
from telebot import types

# --- কনফিগারেশন ---
TOKEN = os.getenv('BOT_TOKEN') # আপনার বটের টোকেন
bot = telebot.TeleBot(TOKEN)

GROUP_LINK = "https://t.me/+EZr3ZIr8Eac0MmE1"
BRAND = "👑 BUMBA PVT LTD 👑"

# --- শক্তিশালী বাইপাস ইঞ্জিন ---
def multi_bypass(url):
    # 🚀 ১ নম্বর ইঞ্জিন: হাই-স্পিড গ্লোবাল বাইপাস এপিআই (ইন্ডিয়াআর্নক্স এর জন্য ১০০% ওয়ার্কিং)
    try:
        api_url = f"https://api.g9bypass.workers.dev/bypass?url={url}"
        response = requests.get(api_url, timeout=12)
        if response.status_code == 200:
            data = response.json()
            # এপিআই রেসপন্স চেক করা হচ্ছে
            if "bypassed" in data and data["bypassed"]:
                return data["bypassed"]
            elif "url" in data and data["url"]:
                return data["url"]
    except Exception:
        pass

    # 🔄 ২ নম্বর ইঞ্জিন: অল্টারনেটিভ প্রিমিয়াম এপিআই গেটওয়ে
    try:
        backup_url = f"https://bypass.dreadful.workers.dev/?url={url}"
        res = requests.get(backup_url, timeout=10).json()
        if "bypassed" in res and res["bypassed"]:
            return res["bypassed"]
    except Exception:
        pass

    return None

# --- স্টার্ট মেসেজ ---
@bot.message_handler(commands=['start'])
def start(message):
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("📢 JOIN OUR GROUP ↗️", url=GROUP_LINK))
    
    welcome_text = (
        f"┌──────────────『 {BRAND} 』──────────────┐\n\n"
        f"👋 **হ্যালো ওস্তাদ, {message.from_user.first_name}!**\n\n"
        "আমি আপনার আল্ট্রা-ফাস্ট বাইপাস টুল। যেকোনো জটিল লিঙ্ক\n"
        "থেকে আসল লিঙ্ক বের করতে জাস্ট লিঙ্কটি পাঠান।\n\n"
        "🚀 **কমান্ড:** `/b [আপনার লিঙ্ক]`\n\n"
        "└────────────────────────────────────────┘"
    )
    bot.send_message(message.chat.id, welcome_text, reply_markup=markup, parse_mode="Markdown")

# --- বাইপাস কমান্ড হ্যান্ডলার ---
@bot.message_handler(commands=['b'])
def handle_b(message):
    args = message.text.split(maxsplit=1)
    if len(args) < 2:
        bot.reply_to(message, "⚠️ **ওস্তাদ, লিঙ্ক দিতে ভুলে গেছেন!**\nসঠিক নিয়ম: `/b https://link.com`", parse_mode="Markdown")
        return

    url = args[1].strip()
    status = bot.reply_to(message, "🔍 **লিঙ্ক অ্যানালাইজ করা হচ্ছে...**\n`[▒▒▒▒▒▒▒▒▒▒] 0%`", parse_mode="Markdown")
    
    time.sleep(0.3)
    bot.edit_message_text("⚡ **ক্লাউডফ্লেয়ার বাইপাস ইঞ্জিন চালু হচ্ছে...**\n`[██████▒▒▒▒] 60%`", status.chat.id, status.message_id, parse_mode="Markdown")
    
    # বাইপাস প্রসেস রান করা হলো
    result = multi_bypass(url)
    
    if result:
        bot.edit_message_text("✅ **বাইপাস সফল!**\n`[██████████] 100%`", status.chat.id, status.message_id, parse_mode="Markdown")
        time.sleep(0.2)
        
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
            "লিঙ্কটির সিকিউরিটি অতিরিক্ত কড়া হওয়ার কারণে এই মুহূর্তে ভাঙা যায়নি।\n\n"
            f"📢 **সহযোগিতার জন্য গ্রুপে জানান:**\n{GROUP_LINK}"
        )
        bot.edit_message_text(error_msg, status.chat.id, status.message_id, reply_markup=error_markup, parse_mode="Markdown", disable_web_page_preview=True)

if __name__ == "__main__":
    bot.infinity_polling()
