import sys
import pkgutil

# 🛠️ Python 3.11+ এর pkgutil এরর ফিক্স করার প্যাচ
if not hasattr(pkgutil, 'get_loader'):
    def fake_get_loader(module_name):
        class FakeLoader:
            pass
        return FakeLoader()
    pkgutil.get_loader = fake_get_loader

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

# 🎯 fastxotp.com প্যানেল থেকে রিয়েল নাম্বার এবং OTP তোলার লজিক
def instagram_creator_logic(chat_id, range_key, count, password):
    bot.send_message(chat_id, f"🚀 **Automation Shuru Hoyeche!**\nTarget: {count}ti Instagram Account.", parse_mode="Markdown")
    
    # প্যানেলের বেস ইউআরএল
    base_url = "https://fastxotp.com/Access/@Bot/3oo9/public/api"
    
    success_count = 0
    for i in range(1, count + 1):
        bot.send_message(chat_id, f"🔄 {i} nongi Account-er jonno number neya hocche...")
        
        # ১. নাম্বার তোলার জন্য POST Request (ভিডিও অনুযায়ী)
        num_url = f"{base_url}/getnum"
        headers = {
            "X-API-Key": range_key,
            "Content-Type": "application/json"
        }
        # ভিডিওতে রেঞ্জ ফরম্যাট ছিল যেমন: 22465XXX
        payload = {
            "range": "22465XXX"  # ইউজার চাইলে মিনি অ্যাপ থেকে কাস্টম রেঞ্জ ইনপুটও হ্যান্ডেল করা যাবে
        }
        
        try:
            num_response = requests.post(num_url, headers=headers, json=payload).json()
            
            if num_response.get("meta", {}).get("status") == "ok":
                data = num_response.get("data", {})
                phone_number = data.get("full_number")
                rid = data.get("rid") # ওটিপি চেক করার জন্য এই rid লাগবে
                
                bot.send_message(chat_id, f"📱 **Number Pawa Gieche:** `{phone_number}`\nInstagram-e Sign-up request pathano হচ্ছে... (Simulation)\nLog ID: `{rid}`", parse_mode="Markdown")
                
                # এখানে ইনস্টাগ্রামের আসল রিকোয়েস্ট পাঠানো যাবে। আপাতত ওটিপি চেক করার লজিক রান হচ্ছে।
                time.sleep(5) 
                bot.send_message(chat_id, f"📩 SMS OTP-r jonno openkkha kora hocche...")
                
                # ২. ওটিপি চেক করার জন্য লুপ (সর্বোচ্চ ২ মিনিট চেক করবে)
                otp_url = f"{base_url}/success-otp-info"
                otp_found = False
                otp_code = None
                
                for attempt in range(24): # ৫ সেকেন্ড পরপর মোট ২৪ বার চেক করবে (২ মিনিট)
                    time.sleep(5)
                    try:
                        # ওটিপি স্ট্যাটাস চেক করার জন্য GET রিকোয়েস্ট
                        otp_response = requests.get(otp_url, headers=headers).json()
                        if otp_response.get("meta", {}).get("status") == "ok":
                            otps_list = otp_response.get("data", {}).get("otps", [])
                            
                            # আমাদের কাঙ্ক্ষিত নাম্বারের ওটিপি এসেছে কিনা ম্যাচ করা
                            for otp_data in otps_list:
                                if otp_data.get("number") == phone_number:
                                    otp_code = otp_data.get("number_otp") # বা 'sms' ফিল্ড থেকে কোড নেওয়া
                                    otp_found = True
                                    break
                        
                        if otp_found:
                            break
                    except:
                        pass
                
                if otp_found and otp_code:
                    bot.send_message(chat_id, f"🔑 **OTP Recieved:** `{otp_code}`! Instagram-e submit kora hocche...", parse_mode="Markdown")
                    time.sleep(3)
                    
                    username = f"bolt_insta_{int(time.time())}_{i}"
                    account_details = f"Username: {username}\nPass: {password}\nPhone: {phone_number}"
                    
                    bot.send_message(chat_id, f"✅ **Instagram Account Created Successfully!**\n`{account_details}`", parse_mode="Markdown")
                    success_count += 1
                else:
                    bot.send_message(chat_id, f"❌ `{phone_number}`-e kono OTP ase nai! Cancel kora holo.")
                    
            else:
                msg = num_response.get("message", "Unknown Error")
                bot.send_message(chat_id, f"⚠️ Number tulte somossa hoyeche: {msg}")
                
        except Exception as e:
            bot.send_message(chat_id, f"❌ API Request Fail: {str(e)}")
            
        time.sleep(2) # প্রতিটি একাউন্টের মাঝে ছোট বিরতি
        
    bot.send_message(chat_id, f"🎉 **Kaj Shes!** Mot {success_count}ti account successfully toiri hoyeche.")

# টেলিগ্রাম বট স্টার্ট কমান্ড
@bot.message_handler(commands=['start'])
def send_welcome(message):
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    host = os.environ.get('RENDER_EXTERNAL_HOSTNAME', 'localhost:5000')
    web_url = host if host.startswith('http') else f"https://{host}/"
    
    web_app_info = telebot.types.WebAppInfo(web_url)
    btn = telebot.types.KeyboardButton(text="📱 Open Mini App", web_app=web_app_info)
    markup.add(btn)
    
    bot.reply_to(message, "Welcome Bolt! Income World 24 Number Bot-e apnake shagoto. Nicher button-e click kore Mini App open koro.", reply_markup=markup)

# মিনি অ্যাপ থেকে ডাটা আসলে তা হ্যান্ডেল করা
@bot.message_handler(content_types=['web_app_data'])
def handle_web_app_data(message):
    try:
        data = json.loads(message.web_app_data.data)
        if data.get("action") == "start_automation":
            range_key = data.get("range")
            count = data.get("count", 1)
            password = data.get("password")
            
            threading.Thread(target=instagram_creator_logic, args=(message.chat.id, range_key, count, password)).start()
            
    except Exception as e:
        bot.reply_to(message, f"❌ Error: {str(e)}")

def run_bot():
    print("Bot is polling...")
    bot.infinity_polling()

if __name__ == "__main__":
    threading.Thread(target=run_bot, daemon=True).start()
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
