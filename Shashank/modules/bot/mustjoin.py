# © By Shashank shukla (Github = itzshukla) You are motherfucker if you Don't gives credits.

from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, Message
from pyrogram.errors import ChatAdminRequired, UserNotParticipant, ChatWriteForbidden
from Shashank import app

#--------------------------
MUST_JOIN1 = "ABOUTT_TOXIC" 
MUST_JOIN2 = "ISHA_BOTS" 
#--------------------------

@app.on_message(filters.incoming & filters.private, group=-1)
async def must_join_channel(app: Client, msg: Message):
    try:
        await app.get_chat_member(MUST_JOIN1, msg.from_user.id)
        await app.get_chat_member(MUST_JOIN2, msg.from_user.id)
    except UserNotParticipant:
        support_link = f"https://t.me/{MUST_JOIN1}"
        update_link = f"https://t.me/{MUST_JOIN2}"
        try:
            await msg.reply_photo(
                photo="https://files.catbox.moe/zuufvl.jpg",
                caption=(
                    f"▪️ ʜᴇʏ ғɪʀsᴛ ᴊᴏɪɴ ᴛᴏ ᴍʏ [sᴜᴘᴘᴏʀᴛ ]({support_link}) "
                    f"& [ᴜᴘᴅᴀᴛᴇ ᴄʜᴀɴɴᴇʟ]({update_link}), ɪғ ʏᴏᴜ ᴡᴀɴᴛ ᴛᴏ ᴜsᴇ ᴍᴇ.\n\n"
                    f"✅ ᴀғᴛᴇʀ ᴊᴏɪɴɪɴɢ, sᴇɴᴅ /start ᴀɢᴀɪɴ!"
                ),
                reply_markup=InlineKeyboardMarkup(
                    [
                        [InlineKeyboardButton("sᴜᴘᴘᴏʀᴛ", url=support_link)],
                        [InlineKeyboardButton("ᴜᴘᴅᴀᴛᴇ", url=update_link)],
                    ]
                )
            )
            await msg.stop_propagation()
        except ChatWriteForbidden:
            pass
    except ChatAdminRequired:
        print(f"⚠️ Please promote me as admin in both {MUST_JOIN1} and {MUST_JOIN2}!")
