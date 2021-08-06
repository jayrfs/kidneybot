import os
from asyncio.exceptions import TimeoutError

from telethon.errors.rpcerrorlist import YouBlockedUserError

from userbot import CMD_HELP, TEMP_DOWNLOAD_DIRECTORY, bot
from userbot.events import register


@register(outgoing=True, pattern=r"^\.bruh(:? |$)([1-8])?")
async def _(bruh):
    await bruh.edit("**Preparing Bruh Sound Effect #2...**")
    level = bruh.pattern_match.group(2)
    if bruh.fwd_from:
        return

    chat = "@bruh_sound_effect_bot"
    message_id_to_reply = bruh.message.reply_to_msg_id
    try:
        async with bruh.client.conversation(chat) as conv:
            try:
                msg = await conv.send_message("/bruh")

                if level:
                    m = f"/bruh {level}"
                    msg_level = await conv.send_message(m, reply_to=msg.id)
                    r = await conv.get_response()

                response = await conv.get_response()
                """ - don't spam notif - """
                await bot.send_read_acknowledge(conv.chat_id)
            except YouBlockedUserError:
                return await bruh.reply("**Please unblock @bruh_sound_effect_bot.**")

            if response.text.startswith("Forward"):
                await bruh.edit(
                    "**Error: Whitelist @bruh_sound_effect_bot in your forward privacy settings.**"
                )
            else:
                downloaded_file_name = await bruh.client.download_media(
                    response.media, TEMP_DOWNLOAD_DIRECTORY
                )
                await bruh.client.send_file(
                    bruh.chat_id,
                    downloaded_file_name,
                    force_document=False,
                    reply_to=message_id_to_reply,
                )
                """ - cleanup chat after completed - """
                try:
                    msg_level
                except NameError:
                    await bruh.client.delete_messages(
                        conv.chat_id, [msg.id, response.id]
                    )
                else:
                    await bruh.client.delete_messages(
                        conv.chat_id, [msg.id, response.id, r.id, msg_level.id]
                    )
    except TimeoutError:
        return await bruh.edit("**Error:** @bruh_sound_effect_bot **is not responding.**")
    await bruh.delete()
    return os.remove(downloaded_file_name)


CMD_HELP.update(
    {
        "bruh": ">`.bruh` or >`.df [level(1-8)]`"
        "\nUsage: bruh"
        "\n@bruh_sound_effect_bot"
    }
)