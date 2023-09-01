from pyrogram.filters import chat
from helpers.mongo import cli

collection = cli["Zaid"]["welcome"]


async def save_welcome(chat_id, msg_id):
    doc = {"_id": 1, "welcomes": {chat_id: msg_id}}
    result = await collection.find_one({"_id": 1})
    if result:
        await collection.update_one(
            {"_id": 1}, {"$set": {f"welcomes.{chat_id}": msg_id}}
        )
    else:
        await collection.insert_one(doc)


async def get_welcome(chat_id):
    result = await collection.find_one({"_id": 1})
    if result is None:
        return None
    try:
        return result["welcomes"][chat_id]
    except KeyError:
        return None


async def clear_welcome(chat_id):
    await collection.update_one({"_id": 1}, {"$unset": {f"welcomes.{chat_id}": ""}})
