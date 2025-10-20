from flask import Flask
import threading
import subprocess

app = Flask(__name__)

def run_bot():
    """यह फंक्शन आपके bot.py स्क्रिप्ट को चलाएगा।"""
    subprocess.run(["python", "bot.py"])

@app.route('/')
def home():
    """यह UptimeRobot को बताने के लिए है कि बॉट जिंदा है।"""
    return "Bot is running!"

if __name__ == "__main__":
    # बॉट को एक अलग थ्रेड में शुरू करें ताकि वेब सर्वर ब्लॉक न हो
    bot_thread = threading.Thread(target=run_bot)
    bot_thread.daemon = True
    bot_thread.start()

    # वेब सर्वर चलाएं
    app.run(host='0.0.0.0', port=5000)
