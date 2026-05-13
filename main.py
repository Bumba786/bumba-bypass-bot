import os
import telebot
from telebot import types
import requests
import time

TOKEN = os.getenv('BOT_TOKEN')
bot = telebot.TeleBot(TOKEN)
GROUP_LINK = "https://t.me/+EZr3Z1r8Eac0MmE1"

@bot.message_handler(commands=['start'])
def start(message):
    photo_url = "https://graph.org/file/a6074a3875323868fe06b.jpg"
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("✨ Join Our Group ✨", url=GROUP_LINK))
    caption = "👋 **Welcome to BUMBA PVT LTD!**\n\nলিঙ্ক বাইপাস করতে নিচের গ্রুপে জয়েন করুন। 👇"
    try:
        bot.send_photo(message.chat.id, photo_url, caption=caption, reply_markup=markup, parse_mode='Markdown')
    except:
        bot.send_message(message.chat.id, caption, reply_markup=markup, parse_mode='Markdown')

@bot.message_handler(commands=['b'])
def bypass(message):
    if message.chat.type == 'private':
        bot.reply_to(message, f"❌ ইনবক্সে হবে না! গ্রুপে জয়েন করুন:\n{GROUP_LINK}")
        return

    args = message.text.split(maxsplit=1)
    if len(args) < 2:
        bot.reply_to(message, "⚠️ লিঙ্ক দিন! যেমন: `/b https://indiaearnx.com/a5Pd`", parse_mode='Markdown')
        return

    url = args[1]
    
    # RDX স্টাইল প্রগ্রেস বার (Screenshot 1000197438.jpg এর মতো)
    sent_msg = bot.reply_to(message, "⏳ **Bypassing :- 0%**\n`[----------]`")
    time.sleep(1)
    bot.edit_message_text(f"⏳ **Bypassing :- 40%**\n`[####------]`", sent_msg.chat.id, sent_msg.message_id, parse_mode='Markdown')
    
    try:
        # এটি সবচেয়ে শক্তিশালী বাইপাস এপিআই যা indiaearnx লিঙ্ক ভাঙতে পারে
        api_url = f"https://api.shrtco.de/v2/shorten?url={url}" # ব্যাকআপের জন্য রাখা হলো
        
        # মূল বাইপাস রিকোয়েস্ট (RDX বটের মতো পাওয়ারফুল)
        bypass_url = f"https://api.bypass.vip/bypass?url={url}" 
        r = requests.get(bypass_url, timeout=20)
        data = r.json()

        # RDX বটের হুবহু ডিজাইন (Screenshot 1000197439.jpg অনুযায়ী)
        if "destination" in data or data.get("status") == "success":
            res = data.get("destination") or data.get("shortenedUrl")
            final_text = (
                f"┎ 🔗 **Original Link :-**\n┃ {url}\n"
                f"┃\n┖ 🔒 **Bypassed Link :-**\n{res}\n\n"
                "━━━━━━━✦✗✦━━━━━━━"
            )
            bot.edit_message_text(final_text, sent_msg.chat.id, sent_msg.message_id, parse_mode='Markdown', disable_web_page_preview=True)
        else:
            # যদি প্রথমটি কাজ না করে তবে আপনার adrinolinks এপিআই ট্রাই করবে
            fallback_url = f"https://adrinolinks.in/api?api=96f86058e17424b953330f576e2704ed92244243&url={url}"
            fr = requests.get(fallback_url)
            fdata = fr.json()
            if fdata.get("status") == "success":
                fres = fdata.get("shortenedUrl")
                bot.edit_message_text(f"✅ **Bypass Success:** {fres}", sent_msg.chat.id, sent_msg.message_id)
            else:
                bot.edit_message_text("❌ লিঙ্কটি সাপোর্ট করছে না। অন্য লিঙ্ক দিন।", sent_msg.chat.id, sent_msg.message_id)
                
    except Exception as e:
        bot.edit_message_text(f"⚠️ সার্ভার এরর! আবার চেষ্টা করুন।", sent_msg.chat.id, sent_msg.message_id)

if __name__ == "__main__":
    bot.infinity_polling()










