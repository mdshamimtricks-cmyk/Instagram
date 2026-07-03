import os
import json
import time
import threading
import requests
import telebot
from flask import Flask, render_template

# Render Environment Variable theke Token nibe
BOT_TOKEN = os.environ.get("BOT_TOKEN", "TUMAR_DIRECT_TOKEN_EKHANE_DITE_PARO")
bot = telebot.TeleBot(BOT_TOKEN)

app = Flask(__name__)

# Web Server Route (Mini App Frontend serve korbe)
@app.route('/')
def home():
    return render_template('index.html')

# Fake/Simulation Instagram Creator Logic (Logic and Flow Working)
def instagram_creator_logic(chat_id, range_key, count, password):
    bot.send_message(chat_id, f"🚀 Automation Prochesh Shuru Hoyeche!\nRange: `{range_key}`\nTarget: {count} Accounts.", parse_mode="Markdown")
    
    success_count = 0
    for i in range(1, count + 1):
        bot.send_message(chat_id, f"🔄 {i} nongi Account-er jonno number neya hocche (Range checking)...")
        time.sleep(3) # Real API requester delay simulation
        
        # Udahoron: Ekhane real SMS code thakbe
        # phone = requests.get(f"https://api.sms-service.com/getNumber?api_key={range_key}").json()
        fake_phone = f"+88018187765{i}3" 
        
        bot.send_message(chat_id, f"📱 Number Pawa Gieche: `{fake_phone}`\nInstagram Sign-up request pathano hocche...")
        time.sleep(4)
        
        bot.send_message(chat_id, f"📩 SMS OTP-r jonno opekkha kora hocche...")
        time.sleep(5)
        
        # Real logic: loop chalate hobe jokhoni OTP asbe code submit hobe
        fake_otp = "543210"
        bot.send_message(chat_id, f"🔑 OTP Recieved: `{fake_otp}`! Submit kora hocche...")
        time.sleep(3)
        
        username = f"user_bolt_{int(time.time())}_{i}"
        
        # Account success hobar por data file-e save/output kora
        account_details = f"Username: {username} | Pass: {password} | 2FA: Active"
        bot.send_message(chat_id, f"✅ Account Created Successfully!\n`{account_details}`", parse_mode="Markdown")
        success_count += 1
        
    bot.send_message(chat_id, f"🎉 Kaj Shes! Mot {success_count}ti account successfully toiri hoyeche.")

# Telegram Bot commands
@bot.message_handler(commands=['start'])
def send_welcome(message):
    # Mini app open korar button standard format
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    web_app_info = telebot.types.WebAppInfo(f"https://{os.environ.get('RENDER_EXTERNAL_HOSTNAME', 'localhost:5000')}/")
    btn = telebot.types.KeyboardButton(text="📱 Open Mini App", web_app=web_app_info)
    markup.add(btn)
    
    bot.reply_to(message, "Welcome to Income World 24 Number Bot! Nicher button-e click kore Mini App open koro.", reply_markup=markup)

# Mini App theke jokhoni data asbe
@bot.message_handler(content_types=['web_app_data'])
def handle_web_app_data(message):
    try:
        data = json.loads(message.web_app_data.data)
        if data.get("action") == "start_automation":
            range_key = data.get("range")
            count = data.get("count", 1)
            password = data.get("password")
            
            # Sub-process run kora jate bot block na hoy
            threading.Thread(target=instagram_creator_logic, args=(message.chat.id, range_key, count, password)).start()
            
    except Exception as e:
        bot.reply_to(message, f"❌ Error processing webapp data: {str(e)}")

# Background-e Bot run korar function
def run_bot():
    print("Bot is polling...")
    bot.infinity_polling()

if __name__ == "__main__":
    # Bot-ke alada Thread-e deya jate Render-er Port error na ase
    threading.Thread(target=run_bot, daemon=True).start()
    
    # Render default PORT local system support handle kora
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
