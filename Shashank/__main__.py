import asyncio
import importlib
import threading
import requests
import time
from flask import Flask

from pyrogram import idle
from Shashank import app, clients, ids
from Shashank.helper import join
from Shashank.modules import ALL_MODULES


# -------------------- FLASK --------------------
flask_app = Flask(__name__)

@flask_app.route('/')
def home():
    return "Bot is alive ✅"

def run_flask():
    flask_app.run(host="0.0.0.0", port=8000)


# -------------------- KEEP ALIVE --------------------
def keep_alive():
    while True:
        try:
            requests.get("https://userbot-r6zm.onrender.com")
        except Exception as e:
            print(f"Ping error: {e}")
        time.sleep(300)


# -------------------- MAIN BOT --------------------
async def start_bot():
    await app.start()
    print("🚀 Bot Started")

    # Import modules
    for module in ALL_MODULES:
        importlib.import_module(f"Shashank.modules{module}")
        print(f"✅ Imported {module}")

    # Start all user clients
    for cli in clients:
        try:
            await cli.start()
            user = await cli.get_me()
            await join(cli)
            ids.append(user.id)
            print(f"🔥 Started {user.first_name}")
        except Exception as e:
            print(f"❌ Client Error: {e}")

    await idle()


# -------------------- RUN --------------------
if __name__ == "__main__":
    # Flask thread
    threading.Thread(target=run_flask).start()

    # Keep alive thread
    threading.Thread(target=keep_alive).start()

    # Run bot (SAFE METHOD)
    asyncio.run(start_bot())
