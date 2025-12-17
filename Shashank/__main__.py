# © By Shashank shukla (Github = itzshukla) You are motherfucker if you Don't gives credits.

import asyncio
import importlib
from pyrogram import Client, idle
from Shashank.helper import join
from Shashank.modules import ALL_MODULES
from Shashank import clients, app, ids
from flask import Flask
import threading
import requests
import time

flask_app = Flask(__name__)

@flask_app.route('/')
def home():
    return "Flask app running on port 8000"

def run_flask():
    flask_app.run(host="0.0.0.0", port=8000)

def keep_alive():
    while True:
        try:
            requests.get("https://userbot-r6zm.onrender.com")
        except Exception as e:
            print(f"Ping error: {e}")
        # Har 5 minute mein ping karein
        time.sleep(300)

async def start_bot():
    await app.start()
    print("LOG: Founded Bot token Booting Zeus.")
    
    for cli in clients:
        try:
            await cli.start()
            ex = await cli.get_me()
            await join(cli)
            print(f"Started {ex.first_name} 🔥")
            ids.append(ex.id)
        except Exception as e:
            print(f"Error: {e}")
    
    await idle()

flask_thread = threading.Thread(target=run_flask)
flask_thread.start()

keep_alive_thread = threading.Thread(target=keep_alive)
keep_alive_thread.start()

loop = asyncio.get_event_loop()
loop.run_until_complete(start_bot())

async def start_bot():
    await app.start()
    print("LOG: ғᴏᴜɴᴅᴇᴅ ʙᴏᴛ ᴛᴏᴋᴇɴ. ʙᴏᴏᴛɪɴɢ ᴛᴏxɪᴄ.")

    for all_module in ALL_MODULES:
        importlib.import_module("Shashank.modules" + all_module)
        print(f"sᴜᴄᴄᴇssғᴜʟʟʏ ɪᴍᴘᴏʀᴛᴇᴅ {all_module} 💥")

    # Start all clients
    for cli in clients:
        try:
            await cli.start()
            ex = await cli.get_me()
            await join(cli)
            print(f"Started {ex.first_name} 🔥")
            ids.append(ex.id)
        except Exception as e:
            print(f"Error starting client: {e}")
    

    await idle()

loop = asyncio.get_event_loop()
loop.run_until_complete(start_bot())
