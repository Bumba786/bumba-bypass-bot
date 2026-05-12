import telebot
import requests

# আপনার টেলিগ্রাম টোকেনটি এখানে সিঙ্গেল কোটেশন (' ') এর ভেতরে দিন
TOKEN = 8839779663:AAG2Sc1p_x_q8BUg2hYAsm3GLgCR1xwXFg8
API = "https://web-production-6701d.up.railway.app/bypass"

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "👋 Welcome to BUMBA PRIVATE BOT!\n\nযেকোনো লিঙ্ক পাঠান, আমি সেটি বাইপাস করে দিচ্ছি।")

@bot.message_handler(func=lambda m: True)
def bypass_link(message):
    url = message.text.strip()
    
    # লিঙ্ক কি না তা চেক করা
    if not url.startswith("http"):
        bot.reply_to(message, "❌ দয়া করে একটি সঠিক URL বা লিঙ্ক পাঠান।")
        return

    bot.reply_to(message, "⏳ BUMBA আপনার লিঙ্কটি প্রসেস করছে... একটু অপেক্ষা করুন।")
    
    try:
        # API তে রিকোয়েস্ট পাঠানো
        r = requests.post(API, json={"url": url})
        res = r.json() # যদি API সরাসরি JSON পাঠায়
        
        bot.send_message(message.chat.id, f"✅ **BUMBA Bypass Success:**\n\n`{res}`", parse_mode="Markdown")
    except Exception as e:
        # যদি JSON কাজ না করে তবে টেক্সট হিসেবে দেখাবে
        try:
            r = requests.post(API, json={"url": url})
            bot.send_message(message.chat.id, f"✅ **BUMBA Bypass Result:**\n\n{r.text}")
        except:
            bot.send_message(message.chat.id, "❌ দুঃখিত, বাইপাস করতে সমস্যা হয়েছে।")

print("BUMBA Bot is running...")
bot.infinity_polling()
