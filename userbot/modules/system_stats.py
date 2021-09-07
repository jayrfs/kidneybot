# Copyright (C) 2019 The Raphielscape Company LLC.
#
# Licensed under the Raphielscape Public License, Version 1.c (the "License");
# you may not use this file except in compliance with the License.
#
""" Userbot module for getting information about the server. """

from asyncio import create_subprocess_exec as asyncrunapp
from asyncio.subprocess import PIPE as asyncPIPE
from os import remove
from platform import python_version, uname
from shutil import which
import requests
from telethon import version
from userbot import ALIVE_NAME, CMD_HELP, KIDNEYBOT_VERSION, UPSTREAM_REPO_BRANCH
from userbot.events import register

# ================= CONSTANT =================
DEFAULTUSER = ALIVE_NAME or "Set `ALIVE_NAME` ConfigVar!"
# ============================================


@register(outgoing=True, pattern=r"^\.sysd$")
async def sysdetails(sysd):
    """For .sysd command, get system info using neofetch."""
    if not sysd.text[0].isalpha() and sysd.text[0] not in ("/", "#", "@", "!"):
        try:
            fetch = await asyncrunapp(
                "neofetch",
                "--stdout",
                stdout=asyncPIPE,
                stderr=asyncPIPE,
            )

            stdout, stderr = await fetch.communicate()
            result = str(stdout.decode().strip()) + str(stderr.decode().strip())

            await sysd.edit("`" + result + "`")
        except FileNotFoundError:
            await sysd.edit("**Install neofetch first!**")


@register(outgoing=True, pattern=r"^\.botver$")
async def bot_ver(event):
    """For .botver command, get the bot version."""
    if event.text[0].isalpha() or event.text[0] in ("/", "#", "@", "!"):
        return
    if which("git") is not None:
        ver = await asyncrunapp(
            "git",
            "describe",
            "--all",
            "--long",
            stdout=asyncPIPE,
            stderr=asyncPIPE,
        )
        stdout, stderr = await ver.communicate()
        verout = str(stdout.decode().strip()) + str(stderr.decode().strip())

        rev = await asyncrunapp(
            "git",
            "rev-list",
            "--all",
            "--count",
            stdout=asyncPIPE,
            stderr=asyncPIPE,
        )
        stdout, stderr = await rev.communicate()
        revout = str(stdout.decode().strip()) + str(stderr.decode().strip())

        await event.edit(f"**Userbot:** `{verout}`\n" f"**Revision:** `{revout}`\n")
    else:
        await event.edit("**Shame that you don't have git!**")


@register(outgoing=True, pattern=r"^\.pip(?: |$)(.*)")
async def pipcheck(pip):
    """For .pip command, do a pip search."""
    if pip.text[0].isalpha() or pip.text[0] in ("/", "#", "@", "!"):
        return
    pipmodule = pip.pattern_match.group(1)
    if pipmodule:
        await pip.edit("**Searching...**")
        pipc = await asyncrunapp(
            "pip3",
            "search",
            pipmodule,
            stdout=asyncPIPE,
            stderr=asyncPIPE,
        )

        stdout, stderr = await pipc.communicate()
        pipout = str(stdout.decode().strip()) + str(stderr.decode().strip())

        if pipout:
            if len(pipout) > 4096:
                await pip.edit("**Output too large, sending as file...**")
                with open("output.txt", "w+") as file:
                    file.write(pipout)
                await pip.client.send_file(
                    pip.chat_id,
                    "output.txt",
                    reply_to=pip.id,
                )
                remove("output.txt")
                return
            await pip.edit(
                "**Query: **\n`"
                f"pip3 search {pipmodule}"
                "`\n**Result: **\n`"
                f"{pipout}"
                "`"
            )
        else:
            await pip.edit(
                "**Query: **\n`"
                f"pip3 search {pipmodule}"
                "`\n**Result: **\n`No result returned/False`"
            )
    else:
        await pip.edit("**Use .help pip to see an example.**")


@register(outgoing=True, pattern=r"^\.alive$")
async def amireallyalive(event):
    """For .alive command, check if the bot is running."""
    await event.delete()
    self_user = await event.client.get_me()
    my_username = self_user.username
    image_url = f"https://robohash.org/set_set4/bgset_bg1/{my_username}kidneybot?size=500x500"
    caption =   (f"<b>KidneyBot v{KIDNEYBOT_VERSION} is alive and kicking!</b>\n"
                f"<b>Telethon:</b> {version.__version__}\n"
                f"<b>Python:</b> {python_version()}\n"
                f"<b>User:</b> {DEFAULTUSER}\n"
                f"<b>Username:</b> {my_username}\n"
                f"<b>Branch:</b> {UPSTREAM_REPO_BRANCH}")
    photo = requests.get(image_url).content

    message_id_to_reply = event.message.reply_to_msg_id

    if not message_id_to_reply:
        message_id_to_reply = None

    try:
        await event.client.send_file(
            event.chat_id,
            photo,
            caption=caption,
            link_preview=False,
            force_document=False,
            reply_to=message_id_to_reply,
            parse_mode=r"html",
        )

    except TypeError:
        await event.edit(caption, parse_mode=r"html")



@register(outgoing=True, pattern=r"^\.aliveu")
async def amireallyaliveuser(username):
    """For .aliveu command, change the username in the .alive command."""
    message = username.text
    if message != ".aliveu" and message[7:8] == " ":
        newuser = message[8:]
        global DEFAULTUSER
        DEFAULTUSER = newuser
    await username.edit(f"**Successfully changed user to** `{newuser}`**!**")


@register(outgoing=True, pattern=r"^\.resetalive$")
async def amireallyalivereset(ureset):
    """For .resetalive command, reset the username in the .alive command."""
    global DEFAULTUSER
    DEFAULTUSER = str(ALIVE_NAME) if ALIVE_NAME else uname().node
    await ureset.edit("**Successfully reset user for alive!**")


CMD_HELP.update(
    {
        "sysd": ">`.sysd`" "\nUsage: Shows system information using neofetch.",
        "botver": ">`.botver`" "\nUsage: Shows the userbot version.",
        "pip": ">`.pip <module(s)>`" "\nUsage: Does a search of pip modules(s).",
        "alive": ">`.alive`"
        "\nUsage: Type .alive to see wether your bot is working or not."
        "\n\n>`.aliveu <text>`"
        "\nUsage: Changes the 'user' in alive to the text you want."
        "\n\n>`.resetalive`"
        "\nUsage: Resets the user to default.",
    }
)
