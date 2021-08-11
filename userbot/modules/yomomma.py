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
        time.sleep(30)
        yomomma=requests.get("https://yomomma-api.herokuapp.com/jokes")
    insult=str(yomomma.content)[11:-3]
    insult2=""
    for i in insult:
        if i=="\\":
            continue
        insult2+=i
    print(insult2)
    await e.edit(insult2)

CMD_HELP.update(
    {
        "yo_momma": ">`.ym`\n\n"
        "sends a yo momma joke.\n can be harsh,\n you have been warned."
        "\nUsage:.ym"
    }
)