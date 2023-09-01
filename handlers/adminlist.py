import html

from pyrogram import filters, Client
from pyrogram.types import Message

from helpers.parser import mention_html, mention_markdown
from handlers.help import *



@Client.on_message(filters.me & filters.command(["admins", "adminlist"], ["."]))
async def adminlist(client: Client, message: Message):
    replyid = None
    toolong = False
    if len(message.text.split()) >= 2:
        chat = message.text.split(None, 1)[1]
    else:
        chat = message.chat.id
    grup = await client.get_chat(chat)
    if message.reply_to_message:
        replyid = message.reply_to_message.message_id
    alladmins = client.iter_chat_members(chat, filter="administrators")
    creator = []
    admin = []
    badmin = []
    async for a in alladmins:
        try:
            nama = f"{a.user.first_name} {a.user.last_name}"
        except:
            nama = a.user.first_name
        if nama is None:
            nama = "☠️ Deleted account"
        if a.status == "administrator":
            if a.user.is_bot:
                badmin.append(mention_markdown(a.user.id, nama))
            else:
                admin.append(mention_markdown(a.user.id, nama))
        elif a.status == "creator":
            creator.append(mention_markdown(a.user.id, nama))
    admin.sort()
    badmin.sort()
    totaladmins = len(creator) + len(admin) + len(badmin)
    teks = f"**Admins in {grup.title}**\n" + "╒═══「 Creator 」\n"
    for x in creator:
        teks += f"│ • {x}\n"
        if len(teks) >= 4096:
            await message.reply(message.chat.id, teks, reply_to_message_id=replyid)
            teks = ""
            toolong = True
    teks += f"╞══「 {len(admin)} Human Administrator 」\n"
    for x in admin:
        teks += f"│ • {x}\n"
        if len(teks) >= 4096:
            await message.reply(message.chat.id, teks, reply_to_message_id=replyid)
            teks = ""
            toolong = True
    teks += f"╞══「 {len(badmin)} Bot Administrator 」\n"
    for x in badmin:
        teks += f"│ • {x}\n"
        if len(teks) >= 4096:
            await message.reply(message.chat.id, teks, reply_to_message_id=replyid)
            teks = ""
            toolong = True
    teks += f"╘══「 Total {totaladmins} Admins 」"
    if toolong:
        await message.reply(message.chat.id, teks, reply_to_message_id=replyid)
    else:
        await message.edit(teks)


@Client.on_message(filters.command(["kickdel", "zombies"], ["."]) & filters.me)
async def kickdel_cmd(client: Client, message: Message):
    await message.edit("<b>Kicking deleted accounts...</b>")
    # noinspection PyTypeChecker
    values = [
        await message.chat.ban_member(user.user.id, int(time()) + 31)
        for member in await message.chat.get_members()
        if member.user.is_deleted
    ]
    await message.edit(f"<b>Successfully kicked {len(values)} deleted account(s)</b>")


@Client.on_message(filters.me & filters.command(["reportadmin", "reportadmins", "report"], ["."]))
async def report_admin(client: Client, message: Message):
    await message.delete()
    if len(message.text.split()) >= 2:
        text = message.text.split(None, 1)[1]
    else:
        text = None
    grup = await client.get_chat(message.chat.id)
    alladmins = client.iter_chat_members(message.chat.id, filter="administrators")
    admin = []
    async for a in alladmins:
        if a.status in ["administrator", "creator"]:
            if not a.user.is_bot:
                admin.append(mention_html(a.user.id, "\u200b"))
    if message.reply_to_message:
        teks = (
            f'{text}'
            if text
            else f'{mention_html(message.reply_to_message.from_user.id, message.reply_to_message.from_user.first_name)} reported to admins.'
        )
    elif text:
        teks = f'{html.escape(text)}'
    else:
        teks = f"Calling admins in {grup.title}."
    teks += "".join(admin)
    if message.reply_to_message:
        await client.send_message(message.chat.id, teks, reply_to_message_id=message.reply_to_message.message_id,
                                  parse_mode="html")
    else:
        await client.send_message(message.chat.id, teks, parse_mode="html")


@Client.on_message(filters.me & filters.command(["everyone", "tagall"], "."))
async def tag_all_users(client: Client, message: Message):
    await message.delete()
    if len(message.text.split()) >= 2:
        text = message.text.split(None, 1)[1]
    else:
        text = "Hi all 🙃"
    kek = client.iter_chat_members(message.chat.id)
    async for a in kek:
        if not a.user.is_bot:
            text += mention_html(a.user.id, "\u200b")
    if message.reply_to_message:
        await client.send_message(message.chat.id, text, reply_to_message_id=message.reply_to_message.message_id,
                                  parse_mode="html")
    else:
        await client.send_message(message.chat.id, text, parse_mode="html")


@Client.on_message(filters.me & filters.command(["botlist", "bots"], ["."]))
async def get_list_bots(client: Client, message: Message):
    replyid = None
    if len(message.text.split()) >= 2:
        chat = message.text.split(None, 1)[1]
    else:
        chat = message.chat.id
    grup = await client.get_chat(chat)
    if message.reply_to_message:
        replyid = message.reply_to_message.message_id
    getbots = client.iter_chat_members(chat)
    bots = []
    async for a in getbots:
        try:
            nama = f"{a.user.first_name} {a.user.last_name}"
        except:
            nama = a.user.first_name
        if nama is None:
            nama = "☠️ Deleted account"
        if a.user.is_bot:
            bots.append(mention_markdown(a.user.id, nama))
    teks = f"**All bots in group {grup.title}**\n" + "╒═══「 Bots 」\n"
    for x in bots:
        teks += f"│ • {x}\n"
    teks += f"╘══「 Total {len(bots)} Bots 」"
    if replyid:
        await client.send_message(message.chat.id, teks, reply_to_message_id=replyid)
    else:
        await message.edit(teks)



add_command_help(
    "adminlist",
    [
        [".admins", "Get chats Admins list."],
        [".kickdel", "To Kick deleted Accounts."],
        [
            ".everyone `or` .tagall",
            "to mention Everyone ",
        ],
        [
            ".botlist",
            "To get Chats Bots list",
        ],
    ],
)




        
