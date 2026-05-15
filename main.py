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
    """আপনার নিজস্ব API এবং উন্নত মেথড ব্যবহার করে বাইপাস"""
    try:
        # মেথড ১: আপনার নিজস্ব Egolinks API (প্রাইভেট)
        api_url = f"https://egolinks.site/api?api={MY_API_KEY}&url={url}"
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        }
        res = requests.get(api_url, headers=headers, timeout=15).json()
        if res.get("status") == "success":
            return res.get("shortened_url")
            
        # মেথড ২: যদি Egolinks ফেল করে, তবে গ্লোবাল বাইপাস ইঞ্জিন ট্রাই করবে
        fallback_url = f"https://api.bypass.vip/bypass?url={url}"
        res2 = requests.get(fallback_url, timeout=12).json()
        if res2.get("status") == "success":
            return res2.get("destination")
            
    except Exception as e:
        print(f"Error: {e}")
    return None

# --- ওয়েলকাম মেসেজ ---
@bot.message_handler(commands=['start'])
def start(message):
    markup = types.InlineKeyboardMarkup()
    # এখানে বাটন ঠিকঠাক আপনার গ্রুপ লিঙ্ক নিয়ে কাজ করবে
    markup.add(types.InlineKeyboardButton("📢 JOIN OFFICIAL GROUP 📢", url=GROUP_LINK))
    
    caption = (
        f"👋 **হ্যালো, {message.from_user.first_name}!**\n\n"
        f"স্বাগতম **{BRAND}** এর অফিসিয়াল বটে।\n"
        "━━━━━━━━━━━━━━━━━━━━\n"
        "আমি উন্নত বাইপাস ইঞ্জিন ব্যবহার করে লিঙ্ক ভাঙতে তৈরি।\n\n"
        "🚀 **কিভাবে ব্যবহার করবেন:**\n"
        "🔗 কমান্ড: `/b [আপনার লিঙ্ক]`\n\n"
        "সব আপডেট পেতে নিচের বাটনে ক্লিক করে আমাদের গ্রুপে জয়েন হোন!"
    )
    try:
        bot.send_photo(message.chat.id, WELCOME_PHOTO, caption=caption, reply_markup=markup, parse_mode="Markdown")
    except:
        bot.send_message(message.chat.id, caption, reply_markup=markup, parse_mode="Markdown")

# --- বাইপাস কমান্ড ---
@bot.message_handler(commands=['b'])
def bypass_handler(message):
    args = message.text.split(maxsplit=1)
    if len(args) < 2:
        bot.reply_to(message, "⚠️ **লিঙ্ক দিন ওস্তাদ!**\nসঠিক নিয়ম: `/b https://link.com`", parse_mode="Markdown")
        return

    url = args[1].strip()
    status = bot.reply_to(message, "🔍 **Processing with Advanced Engines...**\n`▒▒▒▒▒▒▒▒▒▒ 20%`", parse_mode="Markdown")
    
    result = get_bypass(url)
    
    if result:
        time.sleep(0.5)
        bot.edit_message_text("⚡ **Bypass Completed!**\n`██████████ 100%`", status.chat.id, status.message_id, parse_mode="Markdown")
        
        final_msg = (
            f"✅ **SUCCESSFULLY UNLOCKED!**\n\n"
            f"📥 **Original:** `{url}`\n"
            f"📤 **Result:** {result}\n\n"
            f"📢 **Support Group:** [BUMBA SUPPORT]({GROUP_LINK})\n"
            "━━━━━━━━━━━━━━━━━━━━\n"
            f"👑 *Powered by {BRAND}*"
        )
        bot.edit_message_text(final_msg, status.chat.id, status.message_id, parse_mode="Markdown", disable_web_page_preview=True)
    else:
        error_msg = (
            "❌ **বাইপাস করা সম্ভব হয়নি!**\n\n"
            "এই লিঙ্কের সিকিউরিটি বর্তমানে অনেক শক্তিশালী।\n\n"
            f"📢 **আপডেট পেতে জয়েন করুন:** [BUMBA GROUP]({GROUP_LINK})"
        )
        bot.edit_message_text(error_msg, status.chat.id, status.message_id, parse_mode="Markdown", disable_web_page_preview=True)

if __name__ == "__main__":
    bot.infinity_polling()

