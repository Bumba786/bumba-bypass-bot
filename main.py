import os
import telebot
import requests

TOKEN = os.getenv('BOT_TOKEN')
bot = telebot.TeleBot(TOKEN)

# বাইপাস ফাংশন
def get_bypass(url):
    try:
        api_url = f"https://api.bypass.vip/bypass?url={url}"
        response = requests.get(api_url, timeout=10)
        data = response.json()
        if data.get("status") == "success":
            return data.get("destination")
        return None
    except:
        return None

# /start কমান্ড
@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "👋 **Welcome to BUMBA PRIVATE BOT!**\n\nলিঙ্ক বাইপাস করতে ব্যবহার করুন: `/b [link]`\nসাপোর্টেড সাইট দেখতে লিখুন: `/supported`", parse_mode='Markdown')

# /supported কমান্ড
@bot.message_handler(commands=['supported'])
def supported(message):
    bot.reply_to(message, "✅ **Supported Sites:**\n\n- Adrinolinks\n- GPLinks\n- Droplink\n- Linkvertise\n- এবং আরও অনেক!")

# /b কমান্ড (আপনার স্ক্রিনশটের মতো সুন্দর রেজাল্ট দেবে)
@bot.message_handler(commands=['b'])
def bypass(message):
    args = message.text.split(maxsplit=1)
    if len(args) < 2:
        bot.reply_to(message, "⚠️ **ভুল নিয়ম!** এভাবে লিখুন: `/b https://example.com`", parse_mode='Markdown')
        return

    original_link = args[1]
    msg = bot.reply_to(message, "⏳ **BUMBA প্রসেস করছে...**")
    
    result = get_bypass(original_link)
    
    if result:
        response_text = (
            f"🚀 **BUMBA BYPASS BOT**\n\n"
            f"🔗 **Original Link :-**\n{original_link}\n\n"
            f"🔓 **Bypassed Link :-** {result}"
        )
        bot.edit_message_text(response_text, msg.chat.id, msg.message_id, parse_mode='Markdown', disable_web_page_preview=True)
    else:
        bot.edit_message_text("❌ **দুঃখিত! এই লিঙ্কটি বাইপাস করা সম্ভব হয়নি।**", msg.chat.id, msg.message_id)

bot.infinity_polling()



