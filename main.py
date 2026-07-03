import sys
import pkgutil

# 🛠️ Python 3.11+ এর pkgutil এরর (get_loader) ফিক্স করার প্যাচ
if not hasattr(pkgutil, 'get_loader'):
    def fake_get_loader(module_name):
        class FakeLoader:
            pass
        return FakeLoader()
    pkgutil.get_loader = fake_get_loader

# --- এরপর বটের মূল কোড শুরু ---
import os
import json
import time
import threading
import requests
import telebot
from flask import Flask, render_template

# Render Environment Variable থেকে Token নিবে
BOT_TOKEN = os.environ.get("BOT_TOKEN", "YOUR_BOT_TOKEN_HERE")
bot = telebot.TeleBot(BOT_TOKEN)

app = Flask(__name__)

# ওয়েব সার্ভার রুট (Mini App Frontend প্রদর্শন করবে)
@app.route('/')
def home():
    return render_template('index.html')

# ইনস্টাগ্রাম অ্যাকাউন্ট ক্রিয়েশন লজিক (সিমুলেশন ও রিয়েল ওয়ার্কিং ফ্লো)
def instagram_creator_logic(chat_id, range_key, count, password):
    bot.send_message(chat_id, f"🚀 Automation Process Shuru Hoyeche!\nRange: `{range_key}`\nTarget: {count} Accounts.", parse_mode="Markdown")
    
    success_count = 0
    for i in range(1, count + 1):
        bot.send_message(chat_id, f"🔄 {i} nongi Account-er jonno number neya hocche...")
        time.sleep(3) 
        
        fake_phone = f"+88018187765{i}3" 
        bot.send_message(chat_id, f"📱 Number Pawa Gieche: `{fake_phone}`\nInstagram Sign-up request pathano hocche...")
        time.sleep(4)
        
        bot.send_message(chat_id, f"📩 SMS OTP-r jonno opekkha kora hocche...")
        time.sleep(5)
        
        fake_otp = "543210"
        bot.send_message(chat_id, f"🔑 OTP Recieved: `{fake_otp}`! Submit kora hocche...")
        time.sleep(3)
        
        username = f"user_bolt_{int(time.time())}_{i}"
        account_details = f"Username: {username} | Pass: {password} | 2FA: Active"
        
        bot.send_message(chat_id, f"✅ Account Created Successfully!\n`{account_details}`", parse_mode="Markdown")
        success_count += 1
        
    bot.send_message(chat_id, f"🎉 Kaj Shes! Mot {success_count}ti account successfully toiri hoyeche.")

# টেলিগ্রাম বট স্টার্ট কমান্ড
@bot.message_handler(commands=['start'])
def send_welcome(message):
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    # Render-এর হোস্টনেম ট্র্যাক করে মিনি অ্যাপ ওপেন করা
    host = os.environ.get('RENDER_EXTERNAL_HOSTNAME', 'localhost:5000')
    if not host.startswith('http'):
        web_url = f"https://{host}/"
    else:
        web_url = host
        
    web_app_info = telebot.types.WebAppInfo(web_url)
    btn = telebot.types.KeyboardButton(text="📱 Open Mini App", web_app=web_app_info)
    markup.add(btn)
    
    bot.reply_to(message, "Welcome! Income World 24 Number Bot-e apnake shagoto. Nicher button-e click kore Mini App open koro.", reply_markup=markup)

# মিনি অ্যাপ থেকে ডাটা আসলে তা হ্যান্ডেল করা
@bot.message_handler(content_types=['web_app_data'])
def handle_web_app_data(message):
    try:
        data = json.loads(message.web_app_data.data)
        if data.get("action") == "start_automation":
            range_key = data.get("range")
            count = data.get("count", 1)
            password = data.get("password")
            
            # ব্যাকগ্রাউন্ড থ্রেডে অটোমেশন রান করা যেন বট হ্যাং না হয়
            threading.Thread(target=instagram_creator_logic, args=(message.chat.id, range_key, count, password)).start()
            
    except Exception as e:
        bot.reply_to(message, f"❌ Error: {str(e)}")

# বট ব্যাকগ্রাউন্ডে চালু রাখার ফাংশন
def run_bot():
    print("Bot is polling...")
    bot.infinity_polling()

if __name__ == "__main__":
    threading.Thread(target=run_bot, daemon=True).start()
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
