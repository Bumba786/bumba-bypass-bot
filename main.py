import os
import telebot
from telebot import types
import requests

# আপনার বটের টোকেন এবং আপডেট করা গ্রুপ লিঙ্ক
TOKEN = os.getenv('BOT_TOKEN')
bot = telebot.TeleBot(TOKEN)
GROUP_LINK = "https://t.me/+EZr3Z1r8Eac0MmE1"



# /start কমান্ড দিলে স্বাগত জানাবে
@bot.message_handler(commands=['start'])
def start(message):
    # আপনার লগের ফটো এরর এড়াতে try-except ব্যবহার করা হয়েছে
    photo_url = "https://graph.org/file/a6074a3875323868fe06b.jpg"
    
    markup = types.InlineKeyboardMarkup()
    btn_group = types.InlineKeyboardButton("✨ Join Our Group ✨", url=GROUP_LINK)
    markup.add(btn_group)
    
    caption = (
        "**👋 Welcome to BUMBA PVT LTD!**\n\n"
        "আমাদের বটটি ব্যবহার করতে নিচের লিঙ্কে জয়েন করুন।\n"
        "সেখানে লিঙ্ক দিলে আমি সেটি অটোমেটিক বাইপাস করে দেব।\n"
        "গ্রুপ লিঙ্ক নিচে দেওয়া হলো: 👇"
    )
    
    try:
        bot.send_photo(message.chat.id, photo_url, caption=caption, reply_markup=markup, parse_mode='Markdown')
    except Exception:
        # ছবি কাজ না করলে শুধু টেক্সট পাঠাবে যাতে বট ক্রাশ না করে
        bot.send_message(message.chat.id, caption, reply_markup=markup, parse_mode='Markdown')

# বাইপাস কমান্ড (/b) - যা শুধুমাত্র গ্রুপে কাজ করবে
@bot.message_handler(commands=['b'])
def bypass(message):
    # ইনবক্সে কাজ বন্ধ রাখার ফিল্টার
    if message.chat.type == 'private':
        bot.reply_to(message, f"❌ **দুঃখিত!** এই বটটি ইনবক্সে কাজ করবে না। বাইপাস করতে আমাদের গ্রুপে জয়েন করুন: {GROUP_LINK}")
        return

    args = message.text.split(maxsplit=1)
    if len(args) < 2:
        bot.reply_to(message, "⚠️ **লিঙ্ক দিন!** যেমন: `/b [link]`")
        return

    url = args[1]
    user_id = message.from_user.id
    msg = bot.reply_to(message, "⏳ **BUMBA PVT LTD প্রসেস করছে...**")

    # বাইপাস এপিআই কল
    try:
        api_url = f"https://api.diskuze.in/bypass?url={url}"
        r = requests.get(api_url, timeout=10).json()

        if r.get("status") == "success":
            res = r.get("destination")
            response_text = (
                f"🚀 **BUMBA PVT LTD BYPASS SUCCESS**\n\n"
                f"🔗 **Original Link :**\n"
                f"├ `{url}`\n"
                f"└ \n"
                f"🔓 **Bypassed Link :** {res}\n\n"
                f"-------------------\n"
                f"👤 **Requested By :** <a href='tg://user?id={user_id}'>{user_id}</a>"
            )
            bot.edit_message_text(response_text, msg.chat.id, msg.message_id, parse_mode='HTML', disable_web_page_preview=True)
        else:
            bot.edit_message_text("❌ **এই লিঙ্কটি বাইপাস করা সম্ভব হয়নি।**", msg.chat.id, msg.message_id)
    except Exception:
        bot.edit_message_text(f"⚠️ **সার্ভার এরর!** পরে চেষ্টা করুন।", msg.chat.id, msg.message_id)

# বট চালু রাখা
if __name__ == "__main__":
    bot.infinity_polling()






