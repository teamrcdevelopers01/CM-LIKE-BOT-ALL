from flask import Flask
from waitress import serve
import threading
import os
import time

app = Flask(__name__)

@app.route('/')
def home():
    """यह UptimeRobot को बताता है कि सर्वर चल रहा है।"""
    return "Bot is alive!"

def run_bot():
    """यह फंक्शन bot.py को इम्पोर्ट करके चलाता है।"""
    print("Bot thread शुरू हो रहा है...")
    time.sleep(2) # सर्वर को स्थिर होने के लिए 2 सेकंड दें
    try:
        # bot.py से main फंक्शन को यहीं पर इम्पोर्ट करें
        from bot import main
        print("Bot सफलतापूर्वक इम्पोर्ट हो गया। अब बॉट शुरू हो रहा है...")
        main()
    except Exception as e:
        # अगर बॉट में कोई एरर आता है, तो उसे लॉग में दिखाएं
        print("!!!!!! BOT THREAD में एक एरर आया !!!!!!")
        print(f"ERROR: {e}")

if __name__ == '__main__':
    # बॉट को एक अलग थ्रेड में शुरू करें
    bot_thread = threading.Thread(target=run_bot, daemon=True)
    bot_thread.start()

    # Waitress का उपयोग करके वेब सर्वर शुरू करें
    port = int(os.environ.get('PORT', 10000))
    print(f"वेब सर्वर Port {port} पर शुरू हो रहा है...")
    serve(app, host='0.0.0.0', port=port)

