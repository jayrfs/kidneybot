import os, requests, time
from asyncio.exceptions import TimeoutError
from userbot import CMD_HELP, bot
from userbot.events import register

@register(outgoing=True, pattern=r"^\.ddg (.*)")
async def duck_duck_go(ddg_q):
    textx = await ddg_q.get_reply_message()
    qry = ddg_q.pattern_match.group(1)
    if qry:
        query = str(qry)
    elif textx:
        query = textx
        query = query.message
    query_encoded = query.replace(" ", "+")
    ddg_url = "https://duckduckgo.com/?q="+query_encoded+"&kp=-1&kl=us-en&kae=t&kz=1&kf=-1&kaf=1&kac=1&kh=1"
    '''payload = {"format": "json", "url": ddg_url}
    r = requests.get("http://is.gd/create.php", params=payload)'''
    await ddg_q.edit(
        f"Here you are, help yourself. \n\
    [{duckduckgo: query}]({ddg_url})"
    )

CMD_HELP.update(
    {
        "duckduckgo": ">`\t.ddg`\n"
        "search duckduckgo for  given query and return search url"
        "\nUsage:.ddg [query]"
    }
)