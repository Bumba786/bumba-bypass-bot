import os
import telebot
import requests

# Railway-র Environment Variables থেকে টোকেন নেবে
TOKEN = os.getenv('BOT_TOKEN')
bot = telebot.TeleBot(TOKEN)

# বাইপাস ফাংশন
def get_bypass(url):
    try:
        # একটি শক্তিশালী পাবলিক এপিআই
        api_url = f"https://api.bypass.vip/bypass?url={url}"
        response = requests.get(api_url, timeout=10)
        data = response.json()
        
        if data.get("status") == "success":
            return data.get("destination")
        else:
            return f"❌ এরর: {data.get('message', 'এই লিঙ্কটি সাপোর্ট করছে না।')}"
    except Exception as e:
        return "⚠️ সার্ভার বর্তমানে ব্যস্ত আছে, পরে চেষ্টা করুন।"

# /start কমান্ড
@bot.message_handler(commands=['start'])
def send_welcome(message):
    welcome_text = (
        "👋 **স্বাগতম BUMBA PRIVATE BOT-এ!**\n\n"
        "আমি আপনাকে বিভিন্ন শর্টলিঙ্ক বাইপাস করতে সাহায্য করতে পারি।\n\n"
        "📌 **কিভাবে ব্যবহার করবেন:**\n"
        "যেকোনো লিঙ্ক বাইপাস করতে লিখুন: `/b [আপনার লিঙ্ক]`\n\n"
        "উদাহরণ: `/b https://indiaearnx.com/xyz`"
    )
    bot.reply_to(message, welcome_text, parse_mode='Markdown')

# /help কমান্ড
@bot.message_handler(commands=['help'])
def help_command(message):
    help_text = "সাহায্যের জন্য সরাসরি আপনার লিঙ্কটি `/b` লিখে পাঠান। যদি কাজ না করে তবে বুঝবেন ওই লিঙ্কটি এখনো আমাদের সিস্টেমে যোগ করা হয়নি।"
    bot.reply_to(message, help_text)

# /b (Bypass) কমান্ড
@bot.message_handler(commands=['b'])
def bypass_handler(message):
    msg_parts = message.text.split(maxsplit=1)
    
    if len(msg_parts) < 2:
        bot.reply_to(message, "⚠️ ভুল ফরম্যাট! সঠিক নিয়ম: `/b https://yourlink.com`")
        return

    target_url = msg_parts[1]
    bot.reply_to(message, "⏳ **বুম্বা প্রসেস করছে... দয়া করে অপেক্ষা করুন।**")
    
    final_result = get_bypass(target_url)
    bot.reply_to(message, f"✅ **সাফল্য! আপনার লিঙ্ক:**\n\n{final_result}")

# বট চালু রাখা
if __name__ == "__main__":
    bot.infinity_polling()


