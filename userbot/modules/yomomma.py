import os, requests, time
from asyncio.exceptions import TimeoutError
from userbot import CMD_HELP, bot
from userbot.events import register

@register(outgoing=True, pattern=r"^\.ym$")
async def yomomma(e):
    """Yo momma is so fat that she gets group insurance"""
    yomomma=requests.get("https://yomomma-api.herokuapp.com/jokes")
    if str(yomomma.content)[12:-3]=="Rate limit exceeded: 5 per 1 minute":
        await e.edit(
            "**Rate Limited... Waiting 10 second...**")
        time.sleep(10)
        yomomma=requests.get("https://yomomma-api.herokuapp.com/jokes")
    await e.edit(str(yomomma.content)[11:-3])

CMD_HELP.update(
    {
        "yo momma": ">`.ym`"
        "\nUsage:.ym"
    }
)