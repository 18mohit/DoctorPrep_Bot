from app import app as telegram_app
from flask import Flask
import threading

# Minimal Flask app for health check
web_app = Flask(__name__)

@web_app.route('/')
def home():
    return 'Telegram bot is running!'

def run_flask():
    web_app.run(host="0.0.0.0", port=10000)

if __name__ == "__main__":
    # Start Flask in a background thread (for Render), Telegram bot in main thread
    threading.Thread(target=run_flask).start()
    print(">>> Starting Telegram bot polling!")
    telegram_app.run_polling()
