import os
from asyncio.exceptions import TimeoutError

from telethon.errors.rpcerrorlist import YouBlockedUserError

from userbot import CMD_HELP, TEMP_DOWNLOAD_DIRECTORY, bot
from userbot.events import register


@register(outgoing=True, pattern=r"^\.bruh(:? |$)([1-8])?")
async def _(bruh):
    await bruh.edit("**Processing...**")
    level = bruh.pattern_match.group(2)
    if bruh.fwd_from:
        return

    if not bruh.reply_to_msg_id:
        return await bruh.edit("**Reply to a message containing an image!**")

    reply_message = await bruh.get_reply_message()

    if not reply_message.media:
        return await bruh.edit("**Reply to a message containing an image!**")

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
        "\nUsage: deepbruh image/sticker from the reply."
        "\n@bruh_sound_effect_bot"
    }
)


'''@register(outgoing=True, pattern=r"^\.tts(?: |$)([\s\S]*)")
async def text_to_speech(query):
    """For .tts command, a wrapper for Google Text-to-Speech."""

    if query.is_reply and not query.pattern_match.group(1):
        message = await query.get_reply_message()
        message = str(message.message)
    else:
        message = str(query.pattern_match.group(1))

    if not message:
        return await query.edit(
            "**Give a text or reply to a message for Text-to-Speech!**"
        )

    await query.edit("**Processing...**")

    try:
        from userbot.modules.sql_helper.globals import gvarstatus
    except AttributeError:
        return await query.edit("**Running on Non-SQL mode!**")

    if gvarstatus("tts_lang") is not None:
        target_lang = str(gvarstatus("tts_lang"))
    else:
        target_lang = "en"

    try:
        gTTS(message, lang=target_lang)
    except AssertionError:
        return await query.edit(
            "**The text is empty.**\n"
            "Nothing left to speak after pre-precessing, tokenizing and cleaning."
        )
    except ValueError:
        return await query.edit("**Language is not supported.**")
    except RuntimeError:
        return await query.edit("**Error loading the languages dictionary.**")
    tts = gTTS(message, lang=target_lang)
    tts.save("k.mp3")
    with open("k.mp3", "rb") as audio:
        linelist = list(audio)
        linecount = len(linelist)
    if linecount == 1:
        tts = gTTS(message, lang=target_lang)
        tts.save("k.mp3")
    with open("k.mp3"):
        await query.client.send_file(query.chat_id, "k.mp3", voice_note=True)
        os.remove("k.mp3")
    await query.delete()
'''