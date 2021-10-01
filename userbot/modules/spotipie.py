# Ported by @jayrfs

import os
from asyncio.exceptions import TimeoutError

from telethon.errors.rpcerrorlist import YouBlockedUserError

from userbot import CMD_HELP, TEMP_DOWNLOAD_DIRECTORY, bot
from userbot.events import register


@register(outgoing=True, pattern=r"^\.spotipie$")
async def _(event):
    if event.fwd_from:
        return
    chat = "@spotipiebot"
    now = "/now"
    await event.edit("**Processing...**")
    try:
        async with event.client.conversation(chat) as conv:
            try:
                msg = await conv.send_message(now)
                response = await conv.get_response()
                """ - don't spam notif - """
                await bot.send_read_acknowledge(conv.chat_id)
            except YouBlockedUserError:
                await event.reply("**Please unblock** @SpotipieBot**.**")
                return
            if response.text.startswith("You are"):
                await event.edit(
                    "**You seem to be hearing songs in your head master, did you forget to take your meds?**"
                )
                return
            downloaded_file_name = await event.client.download_media(
                response.media, TEMP_DOWNLOAD_DIRECTORY
            )
            link = response.reply_markup.rows[0].buttons[0].url
            await event.client.send_file(
                event.chat_id,
                downloaded_file_name,
                force_document=False,
                caption=f"[Play on Spotify]({link})",
            )
            """ - cleanup chat after completed - """
            await event.client.delete_messages(conv.chat_id, [msg.id, response.id])
    except TimeoutError:
        return await event.edit("**Error:** @spotipiebot **is not responding.**")
    await event.delete()
    return os.remove(downloaded_file_name)

@register(outgoing=True, pattern=r"^\.spotipieb$")
async def _(event):
    if event.fwd_from:
        return
    # if not event.reply_to_msg_id:
    #     return await event.edit("**Reply to a text message.**")
    # reply_message = await event.get_reply_message()
    # if not reply_message.text:
    #     return await event.edit("**Reply to a text message.**")
    chat = "@spotipiebot"
    await event.edit("**Processing...**")

    try:
        async with bot.conversation(chat) as conv:
            try:
                response = conv.wait_event(
                    events.NewMessage(incoming=True, from_users=1662850526)
                )
                await bot.send_message(chat, '/now')
                response = await response
                await bot.send_read_acknowledge(conv.chat_id)

            except YouBlockedUserError:
                return await event.reply("**Please unblock @spotipiebot and try again**")

            if response.text.startswith("Hi!"):
                await event.edit(
                    "**Can you kindly disable your forward privacy settings for good?**"
                )
            else:
                await event.delete()
                await bot.forward_messages(event.chat_id, response.message)

    except TimeoutError:
        return await event.edit("**Error: **@spotipiebot** is not responding.**")


CMD_HELP.update(
    {
        "spotipie": ">`.spotipie` or `spotipieb`"
        ">`.spotipie for hyperlink version and` or `spotipieb for buttonurl version`"
        "\nUsage: Show what you're listening on spotify with blur."
        "\n@spotipiebot"
    }
)
