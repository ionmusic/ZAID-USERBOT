from pyrogram import Client, filters
from pyrogram.types import Message
from handlers.help import *


@Client.on_message(filters.command("duck", ["."]) & filters.me)
async def duckgo(client: Client, message: Message):
    input_str = " ".join(message.command[1:])
    if (
        sample_url := f'https://duckduckgo.com/?q={input_str.replace(" ", "+")}'
    ):
        link = sample_url.rstrip()
        await message.edit_text(
            f"Let me 🦆 DuckDuckGo that for you:\n🔎 [{input_str}]({link})"
        )
    else:
        await message.edit_text("something is wrong. please try again later.")


add_command_help(
    "duckduckgo",
    [
        [".duck", "To Get Link Of Duck Duck Go."],
    ],
)
