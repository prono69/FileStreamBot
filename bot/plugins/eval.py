import asyncio
import sys
import io
import traceback
import os
from time import perf_counter
from hydrogram import filters
from hydrogram.types import Message
from bot import TelegramBot
from bot.config import Telegram

@TelegramBot.on_message(filters.command(["eval", "ev"]) & filters.users(Telegram.OWNER_ID) & ~filters.forwarded)
async def evaluation_cmd_t(client, message: Message):
    if message.from_user.id != 790841356:
        return await message.reply("Only Developer")
    
    status_message = await message.reply("__Processing eval pyrogram...__")
    try:
        cmd = message.text.split(" ", maxsplit=1)[1]
    except IndexError:
        return await status_message.edit("__No evaluate message!__")
    
    old_stdout, old_stderr = sys.stdout, sys.stderr
    sys.stdout, sys.stderr = io.StringIO(), io.StringIO()
    stdout, stderr, exc = None, None, None
    
    try:
        await aexec(cmd, client, message)
    except Exception:
        exc = traceback.format_exc()
    
    stdout, stderr = sys.stdout.getvalue(), sys.stderr.getvalue()
    sys.stdout, sys.stderr = old_stdout, old_stderr
    
    evaluation = exc or stderr or stdout or "Success"
    final_output = f"**OUTPUT**:\n<pre language=''>{evaluation.strip()}</pre>"
    
    if len(final_output) > 4096:
        with open("eval.txt", "w", encoding="utf8") as out_file:
            out_file.write(final_output)
        await status_message.reply_document("eval.txt", caption=cmd[:1024], disable_notification=True)
        os.remove("eval.txt")
        await status_message.delete()
    else:
        await status_message.edit_text(final_output)

async def aexec(code, client, message):
    exec(
        """
async def __aexec(client, message):
    import os
    neo = message
    message = event = neo = e
    r = reply = message.reply_to_message
    chat = message.chat.id
    c = client
    to_photo = message.reply_photo
    to_video = message.reply_video
    p = print
    """ + "\n".join(f" {line}" for line in code.split("\n"))
    )
    return await locals()["__aexec"](client, message)
