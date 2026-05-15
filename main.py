import os
import telebot
import requests
import time
from telebot import types

# --- কনফিগারেশন ---
TOKEN = os.getenv('BOT_TOKEN')
bot = telebot.TeleBot(TOKEN)

# আপনার গ্রুপ লিঙ্ক এবং ব্র্যান্ডিং (১০০% চেক করা)
GROUP_LINK = "https://t.me/+EZr3ZIr8Eac0MmE1"
WELCOME_PHOTO = "https://graph.org/file/a8074a3875323868fe08b.jpg"
BRAND = "⚡ BUMBA PVT LTD ⚡"

def get_bypass_result(url):
    """৩টি শক্তিশালী ইঞ্জিন দিয়ে ট্রাই করবে"""
    # মেথড ১: Egolinks API
    try:
        res = requests.get(f"https://egolinks.site/api?api=5962888691f97750835f83857321520630b9d99c&url={url}", timeout=12).json()
        if res.get("status") == "success": return res.get("shortened_url")
    except: pass

    # মেথড ২: Bypass VIP
    try:
        res = requests.get(f"https://api.bypass.vip/bypass?url={url}", timeout=10).json()
        if res.get("status") == "success": return res.get("destination")
    except: pass

    # মেথড ৩: Droplink API
    try:
        res = requests.get(f"https://droplink.co/api?api=96f86058e17424b89311059f31a19616e0339d37&url={url}", timeout=10).json()
        if res.get("status") == "success": return res.get("shortened_url")
    except: pass
    
    return None

# --- গ্র্যান্ড ওয়েলকাম মেসেজ ---
@bot.message_handler(commands=['start'])
def start(message):
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("📢 JOIN OFFICIAL GROUP 📢", url=GROUP_LINK))
    
    caption = (
        f"👋 **হ্যালো, {message.from_user.first_name}!**\n\n"
        f"👑 **{BRAND} BYPASS BOT**\n"
        "━━━━━━━━━━━━━━━━━━━━\n"
        "আমি আপনার যেকোনো কঠিন লিঙ্ক মুহূর্তেই বাইপাস করে দিতে পারি।\n\n"
        "🚀 **ব্যবহার করবেন কীভাবে:**\n"
        "🔗 `/b [আপনার লিঙ্ক]`\n\n"
        "সব আপডেট পেতে নিচের বাটনে ক্লিক করে আমাদের গ্রুপে জয়েন থাকুন!"
    )
    try:
        bot.send_photo(message.chat.id, WELCOME_PHOTO, caption=caption, reply_markup=markup, parse_mode="Markdown")
    except:
        bot.send_message(message.chat.id, caption, reply_markup=markup, parse_mode="Markdown")

# --- প্রো লেভেল বাইপাস হ্যান্ডলার ---
@bot.message_handler(commands=['b'])
def bypass_handler(message):
    args = message.text.split(maxsplit=1)
    if len(args) < 2:
        bot.reply_to(message, "⚠️ **লিঙ্ক দিতে ভুলে গেছেন ওস্তাদ!**\nসঠিক নিয়ম: `/b https://link.com`", parse_mode="Markdown")
        return

    url = args[1].strip()
    status = bot.reply_to(message, "🔍 **Analyzing Link... 10%**\n`▒▒▒▒▒▒▒▒▒▒`", parse_mode="Markdown")
    
    time.sleep(0.5)
    bot.edit_message_text("⚡ **Bypassing Security... 60%**\n`██████▒▒▒▒`", status.chat.id, status.message_id, parse_mode="Markdown")
    
    result = get_bypass_result(url)
    
    if result:
        time.sleep(0.3)
        bot.edit_message_text("✨ **Success! 100%**\n`██████████`", status.chat.id, status.message_id, parse_mode="Markdown")
        
        final_msg = (
            f"✅ **BYPASS COMPLETED!**\n\n"
            f"📥 **Original:** `{url}`\n"
            f"📤 **Unlocked:** {result}\n\n"
            f"📢 **Join:** [আমাদের গ্রুপে ক্লিক করুন]({GROUP_LINK})\n"
            "━━━━━━━━━━━━━━━━━━━━\n"
            f"👑 *Powered by {BRAND}*"
        )
        bot.edit_message_text(final_msg, status.chat.id, status.message_id, parse_mode="Markdown", disable_web_page_preview=True)
    else:
        error_msg = (
            "❌ **FAILED TO BYPASS!**\n\n"
            "এই লিঙ্কের সিকিউরিটি বর্তমানে অনেক শক্তিশালী। ফ্রি সার্ভার এটি ভাঙতে পারছে না।\n\n"
            f"💡 **আপডেট পেতে গ্রুপে জয়েন করুন:** [BUMBA SUPPORT]({GROUP_LINK})"
        )
        bot.edit_message_text(error_msg, status.chat.id, status.message_id, parse_mode="Markdown", disable_web_page_preview=True)

if __name__ == "__main__":
    bot.infinity_polling()














