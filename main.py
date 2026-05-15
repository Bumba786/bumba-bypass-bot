import os
import telebot
import requests
import time
from telebot import types

# --- কনফিগারেশন ---
TOKEN = os.getenv('BOT_TOKEN')
bot = telebot.TeleBot(TOKEN)

# আপনার গ্রুপ লিঙ্ক (১০০% চেক করা)
GROUP_LINK = "https://t.me/+EZr3ZIr8Eac0MmE1"

# ওয়েলকাম ফটো লিঙ্ক
WELCOME_PHOTO = "https://graph.org/file/a8074a3875323868fe08b.jpg"

def get_bypass(url):
    """Egolinks এবং Bypass VIP দিয়ে লিঙ্ক চেক করার ফাংশন"""
    try:
        # মেথড ১: Egolinks
        ego_url = f"https://egolinks.site/api?api=5962888691f97750835f83857321520630b9d99c&url={url}"
        res = requests.get(ego_url, timeout=15)
        data = res.json()
        if data.get("status") == "success":
            return data.get("shortened_url")
    except:
        pass

    try:
        # মেথড ২: Bypass VIP (ব্যাকআপ)
        res = requests.get(f"https://api.bypass.vip/bypass?url={url}", timeout=15)
        data = res.json()
        if data.get("status") == "success":
            return data.get("destination")
    except:
        pass
    return None

# --- নিউ মেম্বার ওয়েলকাম মেসেজ ---
@bot.message_handler(commands=['start'])
def welcome(message):
    user_name = message.from_user.first_name
    
    # গ্রুপ লিঙ্কের জন্য বাটন
    markup = types.InlineKeyboardMarkup()
    btn_group = types.InlineKeyboardButton("📢 আমাদের গ্রুপে জয়েন করুন 📢", url=GROUP_LINK)
    markup.add(btn_group)
    
    welcome_text = (
        f"👋 **হ্যালো {user_name}!**\n\n"
        "✨ **BUMBA ADVANCE BYPASS BOT**-এ আপনাকে স্বাগতম! ✨\n\n"
        "আমি আপনার দেওয়া কঠিন শর্টনার লিঙ্কগুলো সহজে বাইপাস করতে পারি।\n\n"
        "🚀 **ব্যবহার করবেন কীভাবে:**\n"
        "লিঙ্কটি পাঠান এইভাবে: `/b আপনার_লিঙ্ক` \n\n"
        "সব আপডেট পেতে নিচের বাটনে ক্লিক করে আমাদের গ্রুপে জয়েন থাকুন!"
    )
    
    try:
        bot.send_photo(message.chat.id, WELCOME_PHOTO, caption=welcome_text, reply_markup=markup, parse_mode="Markdown")
    except:
        bot.send_message(message.chat.id, welcome_text, reply_markup=markup, parse_mode="Markdown")

# --- লিঙ্ক বাইপাস কমান্ড ---
@bot.message_handler(commands=['b'])
def bypass_command(message):
    args = message.text.split(maxsplit=1)
    if len(args) < 2:
        bot.reply_to(message, "⚠️ **দয়া করে লিঙ্ক দিন!** \nউদাহরণ: `/b https://indiaearnx.com/xxx`", parse_mode="Markdown")
        return

    url = args[1].strip()
    sent_msg = bot.reply_to(message, "🔄 **অ্যানালাইজ করা হচ্ছে... ১৫%**\n`[##--------]`", parse_mode="Markdown")
    
    time.sleep(0.5)
    bot.edit_message_text("⚡ **সিকিউরিটি ভাঙা হচ্ছে... ৬৫%**\n`[######----]`", sent_msg.chat.id, sent_msg.message_id, parse_mode="Markdown")
    
    result = get_bypass(url)
    
    if result:
        bot.edit_message_text("✨ **সাফল্য! ১০০%**\n`[##########]`", sent_msg.chat.id, sent_msg.message_id, parse_mode="Markdown")
        final_text = (
            "✅ **লিঙ্ক বাইপাস সফল হয়েছে!**\n\n"
            f"📥 **মূল লিঙ্ক:** `{url}`\n"
            f"📤 **বাইপাস লিঙ্ক:** {result}\n\n"
            f"📢 **আপডেট পেতে জয়েন করুন:** [ক্লিক করুন]({GROUP_LINK})"
        )
        bot.edit_message_text(final_text, sent_msg.chat.id, sent_msg.message_id, parse_mode="Markdown", disable_web_page_preview=True)
    else:
        error_text = (
            "❌ **বাইপাস ব্যর্থ হয়েছে!**\n\n"
            "সার্ভার এই লিঙ্কটি প্রসেস করতে পারছে না। RDX বা আদ্রি লিঙ্ক সার্ভার অফলাইন থাকলে এমন হতে পারে।\n\n"
            f"সাহায্যের জন্য আমাদের [গ্রুপে]({GROUP_LINK}) মেসেজ দিন।"
        )
        bot.edit_message_text(error_text, sent_msg.chat.id, sent_msg.message_id, parse_mode="Markdown", disable_web_page_preview=True)

if __name__ == "__main__":
    print("Bot is running...")
    bot.infinity_polling()













