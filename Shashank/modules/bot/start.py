import logging
import random
from pyrogram import Client, filters
from pyrogram.errors import SessionPasswordNeeded
from pyrogram.types import (
    Message, InlineKeyboardMarkup, InlineKeyboardButton,
    CallbackQuery
)
from pymongo import MongoClient
from config import API_ID, API_HASH, MONGO_URL

# -------------------- CONFIG --------------------
ALIVE_PICS = [
    "https://telegra.ph/file/4c8c5c9c2c2e1b9.jpg",
    "https://telegra.ph/file/9b1d2d3c4f5a6b7.jpg"
]

# -------------------- BOT --------------------
app = Client("userbot", api_id=API_ID, api_hash=API_HASH, bot_token=None)

logging.basicConfig(level=logging.INFO)

user_sessions = {}
active_sessions = []

mongo = MongoClient(MONGO_URL)
db = mongo["SessionDB"]
sessions = db["UserSessions"]

# -------------------- BUTTONS --------------------
buttons = InlineKeyboardMarkup([
    [InlineKeyboardButton("⚡ Guide", callback_data="guide")],
    [
        InlineKeyboardButton("❔ Help", callback_data="help"),
        InlineKeyboardButton("📘 About", callback_data="about")
    ]
])

# -------------------- START --------------------
@app.on_message(filters.command("start") & filters.private)
async def start(client: Client, message: Message):

    text = f"""
╭━━━〔 ✦ ɪsʜᴀ ᴜsᴇʀʙᴏᴛ ✦ 〕━━━╮
┃ ✧ ʜᴇʏ {message.from_user.mention}
┃ ✧ ᴡᴇʟᴄᴏᴍᴇ ⚡
┣━━━━━━━━━━━━━━━
┃ ➤ /add - host bot
┃ ➤ /clone - use session
┃ ➤ /remove - logout
╰━━━━━━━━━━━━━━━╯
"""

    photo = random.choice(ALIVE_PICS)

    try:
        await client.send_photo(
            message.chat.id,
            photo,
            caption=text,
            reply_markup=buttons
        )
    except:
        await message.reply_text(text, reply_markup=buttons)

# -------------------- CALLBACK --------------------
@app.on_callback_query()
async def callbacks(client: Client, query: CallbackQuery):
    if query.data == "help":
        await query.message.edit_text("Use /add or /clone")
    elif query.data == "about":
        await query.message.edit_text("Userbot Hosting Bot ⚡")
    elif query.data == "guide":
        await query.message.edit_text("Send /add → phone → OTP → done")

# -------------------- CLONE --------------------
@app.on_message(filters.command("clone") & filters.private)
async def clone(client: Client, msg: Message):
    if len(msg.command) < 2:
        return await msg.reply("❌ Use: /clone session_string")

    session = msg.command[1]
    m = await msg.reply("⏳ Processing...")

    try:
        bot = Client(
            name="clone",
            api_id=API_ID,
            api_hash=API_HASH,
            session_string=session
        )
        await bot.start()
        user = await bot.get_me()

        await m.edit(f"✅ Logged in as {user.first_name}")

    except Exception as e:
        await m.edit(f"❌ Error:\n{e}")

# -------------------- ADD --------------------
@app.on_message(filters.command("add") & filters.private)
async def add(_, message: Message):
    user_sessions[message.from_user.id] = {"step": "phone"}
    await message.reply("📲 Send phone number (+91xxxx)")

# -------------------- REMOVE --------------------
@app.on_message(filters.command("remove") & filters.private)
async def remove(_, msg: Message):
    uid = msg.from_user.id

    if not sessions.find_one({"_id": uid}):
        return await msg.reply("❌ No session found")

    for c in active_sessions:
        if c.name == f"Auto_{uid}":
            await c.stop()
            active_sessions.remove(c)
            break

    sessions.delete_one({"_id": uid})
    await msg.reply("✅ Removed")

# -------------------- SESSION FLOW --------------------
@app.on_message(filters.private & ~filters.command(
    ["start", "add", "remove", "clone"]
))
async def session_handler(_, msg: Message):
    uid = msg.from_user.id
    data = user_sessions.get(uid)

    if not data:
        return

    step = data["step"]

    if step == "phone":
        phone = msg.text.strip()

        client = Client(
            name=f"gen_{uid}",
            api_id=API_ID,
            api_hash=API_HASH,
            in_memory=True
        )

        await client.connect()

        try:
            sent = await client.send_code(phone)
        except Exception as e:
            await msg.reply(f"❌ OTP failed:\n{e}")
            return

        data.update({
            "client": client,
            "phone": phone,
            "hash": sent.phone_code_hash,
            "step": "otp"
        })

        await msg.reply("📨 Send OTP like: 1 2 3 4 5")

    elif step == "otp":
        otp = msg.text.replace(" ", "")
        client = data["client"]

        try:
            await client.sign_in(data["phone"], data["hash"], otp)
        except SessionPasswordNeeded:
            data["step"] = "2fa"
            return await msg.reply("🔐 Send 2FA password")
        except Exception as e:
            await msg.reply(f"❌ Login failed:\n{e}")
            await client.disconnect()
            user_sessions.pop(uid)
            return

        await finalize(client, msg, uid)

    elif step == "2fa":
        client = data["client"]

        try:
            await client.check_password(msg.text.strip())
        except Exception as e:
            await msg.reply(f"❌ Wrong password:\n{e}")
            return

        await finalize(client, msg, uid)

# -------------------- FINAL --------------------
async def finalize(client, msg, uid):
    try:
        string = await client.export_session_string()
        user = await client.get_me()

        sessions.update_one(
            {"_id": uid},
            {"$set": {"session": string}},
            upsert=True
        )

        bot = Client(
            name=f"Auto_{uid}",
            api_id=API_ID,
            api_hash=API_HASH,
            session_string=string
        )

        await bot.start()
        active_sessions.append(bot)

        await msg.reply(f"✅ Logged in as {user.first_name}")

    except Exception as e:
        await msg.reply(f"❌ Error:\n{e}")

    finally:
        await client.disconnect()
        user_sessions.pop(uid, None)

# -------------------- RUN --------------------
app.run()
