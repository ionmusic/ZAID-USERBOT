from pyrogram.filters import chat
from helpers.mongo import cli

collection = cli["Zaid"]["notes"]


async def save_note(note_name, note_id):
    doc = {"_id": 1, "notes": {note_name: note_id}}
    result = await collection.find_one({"_id": 1})
    if result:
        await collection.update_one(
            {"_id": 1}, {"$set": {f"notes.{note_name}": note_id}}
        )
    else:
        await collection.insert_one(doc)


async def get_note(note_name):
    result = await collection.find_one({"_id": 1})
    if result is None:
        return None
    try:
        return result["notes"][note_name]
    except KeyError:
        return None


async def rm_note(note_name):
    await collection.update_one({"_id": 1}, {"$unset": {f"notes.{note_name}": ""}})


async def all_notes():
    results = await collection.find_one({"_id": 1})
    try:
        notes_dic = results["notes"]
        return notes_dic.keys()
    except:
        return None


async def rm_all():
    await collection.update_one({"_id": 1}, {"$unset": {"notes": ""}})
