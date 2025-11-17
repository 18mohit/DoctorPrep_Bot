from flask import Flask
import threading
import app  # your telegram bot file

web_app = Flask(__name__)

@web_app.route('/')
def home():
    return 'Telegram bot is running!'

def run_telegram_bot():
    print(">>> Starting Telegram bot polling!")
    try:
        app.run_polling()
    except Exception as e:
        print("Telegram bot crashed with exception:", e)

if __name__ == "__main__":
    threading.Thread(target=run_telegram_bot).start()
    web_app.run(host='0.0.0.0', port=10000)
