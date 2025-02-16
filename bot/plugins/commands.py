import random
from hydrogram import filters
from hydrogram.types import Message
from bot import TelegramBot
from bot.config import Telegram, PICS
from bot.modules.static import *
from bot.modules.decorators import verify_user

@TelegramBot.on_message(filters.command(['start', 'help']) & filters.private)
@verify_user
async def start_command(_, msg: Message):
    # Randomly select a photo link from PICS
    pic = random.choice(PICS.split())
    caption_text = random.choice(WelcomeText) % {'first_name': msg.from_user.first_name}
    
    try:
        await msg.reply_photo(
            photo=pic,
            caption=caption_text,
            quote=True
        )
    except Exception:
        # If sending the photo fails, just send the text message.
        await msg.reply(
            text=caption_text,
            quote=True
        )
    
    
@TelegramBot.on_message(filters.command('privacy') & filters.private)
@verify_user
async def privacy_command(_, msg: Message):
    await msg.reply(text=PrivacyText, quote=True, disable_web_page_preview=True)

@TelegramBot.on_message(filters.command('log') & filters.chat(Telegram.OWNER_ID))
async def log_command(_, msg: Message):
    await msg.reply_document('event-log.txt', quote=True)
