import os
import telebot
from telebot import types
import requests

# পরিবেশ ভেরিয়েবল থেকে টোকেন সংগ্রহ
TOKEN = os.getenv('BOT_TOKEN')
bot = telebot.TeleBot(TOKEN)
GROUP_LINK = "https://t.me/+EZr3Z1r8Eac0MmE1"

# /start কমান্ড হ্যান্ডলার
@bot.message_handler(commands=['start'])
def start(message):
    photo_url = "https://graph.org/file/a6074a3875323868fe06b.jpg"
    markup = types.InlineKeyboardMarkup()
    btn_group = types.InlineKeyboardButton("✨ Join Our Group ✨", url=GROUP_LINK)
    markup.add(btn_group)
    
    caption = "👋 **Welcome to BUMBA PVT LTD!**\n\nলিঙ্ক বাইপাস করতে নিচের বাটনে ক্লিক করে আমাদের গ্রুপে জয়েন করুন। 👇"
    
    try:
        bot.send_photo(message.chat.id, photo_url, caption=caption, reply_markup=markup, parse_mode='Markdown')
    except Exception:
        bot.send_message(message.chat.id, caption, reply_markup=markup, parse_mode='Markdown')

# বাইপাস কমান্ড হ্যান্ডলার (/b)
@bot.message_handler(commands=['b'])
def bypass(message):
    # শুধুমাত্র গ্রুপে কাজ করার শর্ত
    if message.chat.type == 'private':
        bot.reply_to(message, f"❌ দুঃখিত! এই বটটি ইনবক্সে কাজ করবে না। বাইপাস করতে গ্রুপে জয়েন করুন:\n{GROUP_LINK}")
        return

    # ইউজার লিঙ্ক দিয়েছে কি না চেক করা
    args = message.text.split(maxsplit=1)
    if len(args) < 2:
        bot.reply_to(message, "⚠️ **ভুল পদ্ধতি!**\nসঠিক নিয়ম: `/b [লিঙ্ক]`\nউদাহরণ: `/b https://indiaearnx.com/a5Pd`", parse_mode='Markdown')
        return

    url = args[1]
    msg = bot.reply_to(message, "⏳ **BUMBA PVT LTD প্রসেস করছে...**")

    # বাইপাস এপিআই কল
    try:
        # এখানে 'api?api=' এর পর সরাসরি কি এবং শেষে '&url=' ঠিকভাবে দেওয়া হয়েছে
        api_url = f"https://adrinolinks.in/api?api=96f86058e17424b953330f576e2704ed92244243&url={url}"
        r = requests.get(api_url, timeout=20)
        data = r.json()

        if data.get("status") == "success":
            short_link = data.get("shortenedUrl")
            response_text = (
                "🚀 **BYPASS SUCCESS**\n\n"
                f"🔓 **Destination Link:** `{short_link}`\n\n"
                "---"
            )
            bot.edit_message_text(response_text, msg.chat.id, msg.message_id, parse_mode='Markdown')
        else:
            bot.edit_message_text("❌ এই লিঙ্কটি বাইপাস করা সম্ভব হয়নি। লিঙ্কটি সঠিক কি না চেক করুন।", msg.chat.id, msg.message_id)
            
    except Exception as e:
        bot.edit_message_text("⚠️ **সার্ভার এরর!** বর্তমানে এপিআই সার্ভারটি ব্যস্ত। দয়া করে কিছুক্ষণ পর আবার চেষ্টা করুন।", msg.chat.id, msg.message_id)

# বট চালু রাখা
if __name__ == "__main__":
    print("Bot is running...")
    bot.infinity_polling()








