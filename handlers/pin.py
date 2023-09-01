from pyrogram import Client, filters
import asyncio
import time
from pyrogram.types import ChatPermissions, Message


@Client.on_message(filters.command("pin", ["."]) & filters.me)
async def pin_message(client: Client, message):
    msg_id=message.message_id
    chat_id=message.chat.id
    if message.reply_to_message is None:
        await client.edit_message_text(chat_id , msg_id , "Shall I pin your head to wall ?")
    elif message.chat.type == "private":
        reply_msg_id=message.reply_to_message.message_id
        await client.pin_chat_message(chat_id , reply_msg_id , both_sides=True)
        await message.edit_text("Done the Job master !")
    else:
        zuzu= await client.get_chat_member(chat_id , "me")
        can_pin=zuzu.can_pin_messages
        if can_pin:         
            reply_msg_id=message.reply_to_message.message_id
            await client.pin_chat_message(chat_id , reply_msg_id)
            await client.edit_message_text(chat_id , msg_id , "Done the Job master !")

        else:
            await client.edit_message_text(chat_id , msg_id , "Not a admin bruh 🥱")
