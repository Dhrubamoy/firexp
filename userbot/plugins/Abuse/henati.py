from telethon import events
from telethon.errors.rpcerrorlist import YouBlockedUserError
from telethon.tl import functions, types

from . import *


@borg.on(admin_cmd(pattern="hpic?(.*)"))
async def _(event):
    if event.fwd_from:
        return
    input_str = event.pattern_match.group(1)
    await event.get_reply_message()
    chat = "@LoliHeavenBot"
    await event.edit("```Checking...```")
    async with event.client.conversation(chat) as conv:
        try:
            response = conv.wait_event(
                events.NewMessage(incoming=True, from_users=986872829)
            )
            await event.client.send_message(chat, "Lolis{}".format(input_str))
            response = await response
        except YouBlockedUserError:
            await event.reply("```Unblock @LoliHeavenBot```")
            return
        if response.text.startswith("I can't find that"):
            await event.edit("😐")
        else:
            await event.delete()
            xxxx = await event.client.send_file(event.chat_id, response.message)
            await unsave_gif(xxxx)
CmdHelp("hentaipic").add_command(
    "hpic", "Uses of this cmnd you get anime porn image"
).add_info(
    "+18 contant"
).add()