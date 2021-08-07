import os, requests
from asyncio.exceptions import TimeoutError
from userbot import CMD_HELP, bot
from userbot.events import register

@register(outgoing=True, pattern=r"^\.ym$")
async def insult(e):
    """Yo momma is so fat that she gets group insurance"""
    yomomma=requests.get("https://yomomma-api.herokuapp.com/jokes")
    await e.edit(str(yomomma.content)[11:-3])

CMD_HELP.update(
    {
        "yoamma": ">`.yomamma` or >`.ym`"
        "\nUsage: yomamma"
    }
)