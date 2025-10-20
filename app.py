from flask import Flask
import threading
from waitress import serve
import os

# यह सुनिश्चित करता है कि main() फंक्शन को इम्पोर्ट किया जा सकता है
if __name__ != '__main__':
    from bot import main as bot_main

app = Flask(__name__)

@app.route('/')
def home():
    """यह UptimeRobot को बताने के लिए है कि बॉट जिंदा है।"""
    return "Bot is alive and running!"

def run_bot():
    """यह फंक्शन bot.py के main फंक्शन को चलाएगा।"""
    # यहाँ हम bot.py से main फंक्शन को कॉल करते हैं
    # यह कोड केवल तभी चलेगा जब यह फ़ाइल सीधे न चलाई जा रही हो
    if 'bot_main' in globals():
        bot_main()

if __name__ == '__main__':
    # बॉट को एक अलग थ्रेड में शुरू करें ताकि वेब सर्वर ब्लॉक न हो
    bot_thread = threading.Thread(target=run_bot, daemon=True)
    bot_thread.start()
    
    # Waitress सर्वर का उपयोग करें जो gunicorn से बेहतर काम करता है
    serve(app, host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
