import os
import telebot
import requests
import time
from telebot import types

# --- কনফিগারেশন ---
TOKEN = os.getenv('BOT_TOKEN')
bot = telebot.TeleBot(TOKEN)

# আপনার তথ্য
GROUP_LINK = "https://t.me/+EZr3ZIr8Eac0MmE1"
MY_API_KEY = "adec84f7928c09e3aa63531c5be3b240d12e25c6"
BRAND = "👑 BUMBA PVT LTD 👑"
WELCOME_PHOTO = "https://graph.org/file/a8074a3875323868fe08b.jpg"

def get_bypass(url):
    """আপনার নিজস্ব API ব্যবহার করে বাইপাস মেথড"""
    try:
        # Egolinks API Call
        api_url = f"https://egolinks.site/api?api={MY_API_KEY}&url={url}"
        res = requests.get(api_url, timeout=15).json()
        if res.get("status") == "success":
            return res.get("shortened_url")
    except:
        pass
    return None

# --- ওয়েলকাম মেসেজ ---
@bot.message_handler(commands=['start'])
def start(message):
    markup = types.InlineKeyboardMarkup()
    # গ্রুপ লিঙ্ক বাটন
    markup.add(types.InlineKeyboardButton("📢 JOIN OFFICIAL GROUP 📢", url=GROUP_LINK))
    
    caption = (
        f"👋 **হ্যালো, {message.from_user.first_name}!**\n\n"
        f"স্বাগতম **{BRAND}** এর অফিসিয়াল বটে।\n"
        "━━━━━━━━━━━━━━━━━━━━\n"
        "আমি আপনার নিজস্ব API ব্যবহার করে লিঙ্ক বাইপাস করতে তৈরি।\n\n"
        "🚀 **কিভাবে ব্যবহার করবেন:**\n"
        "🔗 কমান্ড লিখুন: `/b [আপনার লিঙ্ক]`\n\n"
        "সব আপডেট পেতে নিচের বাটনে ক্লিক করে গ্রুপে জয়েন হোন!"
    )
    try:
        bot.send_photo(message.chat.id, WELCOME_PHOTO, caption=caption, reply_markup=markup, parse_mode="Markdown")
    except:
        bot.send_message(message.chat.id, caption, reply_markup=markup, parse_mode="Markdown")

# --- বাইপাস প্রসেসর ---
@bot.message_handler(commands=['b'])
def bypass_handler(message):
    args = message.text.split(maxsplit=1)
    if len(args) < 2:
        bot.reply_to(message, "⚠️ **লিঙ্ক দিতে হবে ওস্তাদ!**\nসঠিক নিয়ম: `/b https://link.com`", parse_mode="Markdown")
        return

    url = args[1].strip()
    status = bot.reply_to(message, "🔍 **Analyzing with Private API...**\n`▒▒▒▒▒▒▒▒▒▒ 15%`", parse_mode="Markdown")
    
    # বাইপাস রেজাল্ট
    result = get_bypass(url)
    
    if result:
        time.sleep(0.5)
        bot.edit_message_text("⚡ **Security Unlocked!**\n`██████████ 100%`", status.chat.id, status.message_id, parse_mode="Markdown")
        
        final_msg = (
            f"✅ **BYPASS SUCCESSFUL!**\n\n"
            f"📥 **লিঙ্ক:** `{url}`\n"
            f"📤 **বাইপাস লিঙ্ক:** {result}\n\n"
            f"📢 **গ্রুপ লিঙ্ক:** [BUMBA SUPPORT]({GROUP_LINK})\n"
            "━━━━━━━━━━━━━━━━━━━━\n"
            f"👑 *Powered by {BRAND}*"
        )
        bot.edit_message_text(final_msg, status.chat.id, status.message_id, parse_mode="Markdown", disable_web_page_preview=True)
    else:
        error_msg = (
            "❌ **বাইপাস ব্যর্থ হয়েছে!**\n\n"
            "এই লিঙ্কের সিকিউরিটি বর্তমানে অনেক শক্তিশালী। আপনার Egolinks API এটি প্রসেস করতে পারছে না।\n\n"
            f"📢 **আপডেট পেতে গ্রুপে জয়েন করুন:** [ক্লিক করুন]({GROUP_LINK})"
        )
        bot.edit_message_text(error_msg, status.chat.id, status.message_id, parse_mode="Markdown", disable_web_page_preview=True)

if __name__ == "__main__":
    bot.infinity_polling()















