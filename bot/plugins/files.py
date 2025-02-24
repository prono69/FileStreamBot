from hydrogram import filters
from hydrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from secrets import token_hex
from bot import TelegramBot
from bot.config import Telegram, Server
from bot.modules.decorators import verify_user
from bot.modules.static import *
from bot.utils import humanbytes

@TelegramBot.on_message(
    filters.private
    & (
        filters.document
        | filters.video
        | filters.video_note
        | filters.audio
        | filters.voice
        | filters.photo
    )
)
@verify_user
async def handle_user_file(_, msg: Message):
    sender_id = msg.from_user.id
    secret_code = token_hex(Telegram.SECRET_CODE_LENGTH)

    # Determine the file type and extract file name and size dynamically
    file_type = None
    if msg.document:
        file_type = "document"
    elif msg.video:
        file_type = "video"
    elif msg.video_note:
        file_type = "video_note"
    elif msg.audio:
        file_type = "audio"
    elif msg.voice:
        file_type = "voice"
    elif msg.photo:
        file_type = "photo"

    # Use getattr to dynamically access file_name and file_size
    file_name = getattr(msg, file_type).file_name if hasattr(getattr(msg, file_type), 'file_name') else file_type.title()
    file_size = getattr(getattr(msg, file_type), 'file_size', 0)
    file = await msg.copy(
        chat_id=Telegram.CHANNEL_ID,
        caption=f'||{secret_code}/{sender_id}||'
    )
    file_id = file.id
    dl_link = f'{Server.BASE_URL}/dl/{file_id}?code={secret_code}'
    stream_link = f'{Server.BASE_URL}/stream/{file_id}?code={secret_code}'
    formatted_message = MediaLinkText.format(file_name=file_name, file_size=humanbytes(file_size), dl_link=dl_link, stream_link=stream_link)
    file_message = FileLinkText.format(file_name=file_name, file_size=humanbytes(file_size), dl_link=dl_link)

    if (msg.document and 'video' in msg.document.mime_type) or msg.video:
        await msg.reply(
            text=formatted_message,
            quote=True,
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton('Download', url=dl_link),
                        InlineKeyboardButton('Stream', url=stream_link)
                    ],
                    [
                        InlineKeyboardButton('Revoke', callback_data=f'rm_{file_id}_{secret_code}')
                    ]
                ]
            )
        )
    else:
        await msg.reply(
            text=file_message,
            quote=True,
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton('Download', url=dl_link),
                        InlineKeyboardButton('Revoke', callback_data=f'rm_{file_id}_{secret_code}')
                    ]
                ]
            )
        )
