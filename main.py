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

# 🎯 fastxotp.com প্যানেল থেকে রিয়েল নাম্বার এবং OTP তোলার ফুল ফিক্সড লজিক
def instagram_creator_logic(chat_id, range_key, count, password):
    bot.send_message(chat_id, f"🚀 **Automation Shuru Hoyeche!**\nTarget: {count}ti Instagram Account.", parse_mode="Markdown")
    
    # 🔗 ফাস্টএক্সওটিপি প্যানেলের একদম সঠিক রিয়েল ইউআরএল
    num_url = "https://fastxotp.com/Access/@Bot/3oo9/public/api/getnum"
    otp_url = "https://fastxotp.com/Access/@Bot/3oo9/public/api/success-otp-info"
    
    # 🔑 ভিডিও থেকে নেওয়া তোমার আসল অ্যাকাউন্ট এপিআই কি
    headers = {
        "X-API-Key": "MURAD_FD980978DCC0298BA17259D8",
        "Content-Type": "application/json"
    }
    
    success_count = 0
    for i in range(1, count + 1):
        bot.send_message(chat_id, f"🔄 {i} nongi Account-er jonno number neya hocche...")
        
        # মিনি অ্যাপে ইউজার যে রেঞ্জ (যেমন: 22465XXX) ইনপুট দিবে তা বডিতে যাবে
        payload = {
            "range": str(range_key).strip()
        }
        
        try:
            # প্যানেল থেকে নাম্বার তোলার জন্য রিকোয়েস্ট
            response = requests.post(num_url, headers=headers, json=payload)
            
            if response.status_code == 200:
                try:
                    num_response = response.json()
                except json.JSONDecodeError:
                    bot.send_message(chat_id, "❌ Response was not valid JSON.")
                    continue
                
                if num_response.get("meta", {}).get("status") == "ok":
                    data = num_response.get("data", {})
                    phone_number = data.get("full_number")
                    rid = data.get("rid") 
                    
                    bot.send_message(chat_id, f"📱 **Number Pawa Gieche:** `{phone_number}`\nLog ID: `{rid}`\n📩 SMS OTP-r jonno opekkha kora hocche...", parse_mode="Markdown")
                    
                    # ⏳ ওটিপি চেকিং লুপ (সর্বোচ্চ ২ মিনিট চেক করবে)
                    otp_found = False
                    otp_code = None
                    
                    for attempt in range(24): 
                        time.sleep(5)
                        try:
                            otp_resp = requests.get(otp_url, headers=headers)
                            if otp_resp.status_code == 200:
                                otp_response = otp_resp.json()
                                if otp_response.get("meta", {}).get("status") == "ok":
                                    otps_list = otp_response.get("data", {}).get("otps", [])
                                    
                                    # আমাদের তোলা নাম্বারের ওটিপি ম্যাচ করানো
                                    for otp_data in otps_list:
                                        if str(otp_data.get("number")) == str(phone_number):
                                            otp_code = otp_data.get("otp") 
                                            otp_found = True
                                            break
                                if otp_found:
                                    break
                        except:
                            pass
                    
                    if otp_found and otp_code:
                        bot.send_message(chat_id, f"🔑 **OTP Recieved:** `{otp_code}`!", parse_mode="Markdown")
                        username = f"user_bolt_{int(time.time())}_{i}"
                        
                        account_details = f"Username: {username}\nPass: {password}\nPhone: {phone_number}\n2FA: Active"
                        bot.send_message(chat_id, f"✅ **Account Created Successfully!**\n`{account_details}`", parse_mode="Markdown")
                        success_count += 1
                    else:
                        bot.send_message(chat_id, f"❌ `{phone_number}`-e kono OTP ase nai! Cancel kora holo.")
                else:
                    msg = num_response.get("message", "Out of stock or invalid range")
                    bot.send_message(chat_id, f"⚠️ Pannel Response: {msg}")
            else:
                bot.send_message(chat_id, f"❌ Server Error! Status Code: {response.status_code}")
                
        except Exception as e:
            bot.send_message(chat_id, f"❌ Request Fail: {str(e)}")
            
        time.sleep(2)
        
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

# মিনি অ্যাপ থেকে ডাটা হ্যান্ডেল করা
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
    bot.infinity_polling(non_stop=True, skip_pending=True)

if __name__ == "__main__":
    threading.Thread(target=run_bot, daemon=True).start()
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
