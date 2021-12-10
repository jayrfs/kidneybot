# Ported by @jayrfs

import os
from asyncio.exceptions import TimeoutError

from telethon.errors.rpcerrorlist import YouBlockedUserError

from userbot import CMD_HELP, TEMP_DOWNLOAD_DIRECTORY, bot
from userbot.events import register
from telethon import events

@register(outgoing=True, pattern=r"^\.revimgsearch$")
async def _(revsearch):
    await revsearch.edit("**Processing...**")
    level = revsearch.pattern_match.group(2)
    if revsearch.fwd_from:
        return

    if not revsearch.reply_to_msg_id:
        return await revsearch.edit("**Reply to a message containing an image!**")

    reply_message = await revsearch.get_reply_message()

    if not reply_message.media:
        return await revsearch.edit("**Reply to a message containing an image!**")

    chat = "@LCxRvsImgSrch_bot"
    message_id_to_reply = revsearch.message.reply_to_msg_id
    try:
        async with revsearch.client.conversation(chat) as conv:
            try:
                msg = await conv.send_message(reply_message)

                response = await conv.get_response()
                """ - don't spam notif - """
                await bot.send_read_acknowledge(conv.chat_id)
            except YouBlockedUserError:
                return await revsearch.reply("**Please unblock @LCxRvsImgSrch_bot.**")

            if response.text.startswith("Forward"):
                await revsearch.edit(
                    "**Error: Whitelist @LCxRvsImgSrch_bot in your forward privacy settings.**"
                )
            else:
                downloaded_file_name = await revsearch.client.download_media(
                    response.media, TEMP_DOWNLOAD_DIRECTORY
                )
                await revsearch.client.send_file(
                    revsearch.chat_id,
                    downloaded_file_name,
                    force_document=False,
                    reply_to=message_id_to_reply,
                )
                """ - cleanup chat after completed - """
                try:
                    msg_level
                except NameError:
                    await revsearch.client.delete_messages(
                        conv.chat_id, [msg.id, response.id]
                    )
                else:
                    await revsearch.client.delete_messages(
                        conv.chat_id, [msg.id, response.id, r.id, msg_level.id]
                    )
    except TimeoutError:
        return await revsearch.edit("**Error:** @LCxRvsImgSrch_bot **is not responding.**")
    await revsearch.delete()
    return os.remove(downloaded_file_name)

@register(outgoing=True, pattern=r"^\.revimgsearch$")
async def _(event):
    if event.fwd_from:
        return
    # if not event.reply_to_msg_id:
    #     return await event.edit("**Reply to a text message.**")
    # reply_message = await event.get_reply_message()
    # if not reply_message.text:
    #     return await event.edit("**Reply to a text message.**")
    chat = "@LCxRvsImgSrch_bot"
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
                return await event.reply("**Please unblock @LCxRvsImgSrch_bot and try again**")

            if response.text.startswith("Hi!"):
                await event.edit(
                    "**Can you kindly disable your forward privacy settings for good?**"
                )
            else:
                await event.delete()
                await bot.forward_messages(event.chat_id, response.message)

    except TimeoutError:
        return await event.edit("**Error: **@LCxRvsImgSrch_bot** is not responding.**")


CMD_HELP.update(
    {
        "revimgsearch": ">`.revimgsearch`"
        "\n>`Reply to an image or a url of an image with `.revimgsearch`"
        "\nCourtesy: @LCxRvsImgSrch_bot"
    }
)
