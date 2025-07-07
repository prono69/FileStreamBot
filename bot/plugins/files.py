from hydrogram import filters
from hydrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from secrets import token_hex
from bot import TelegramBot
from bot.config import Telegram, Server
from bot.modules.decorators import verify_user
from bot.modules.static import *
from bot.utils import humanbytes
import mimetypes
from pathlib import Path

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

    # Initialize variables
    file_type = None
    mime_type = None
    file_name = "file"
    
    # Determine file type and get metadata
    if msg.document:
        file_type = "document"
        mime_type = msg.document.mime_type
        file_name = msg.document.file_name or "document"
    elif msg.video:
        file_type = "video"
        mime_type = msg.video.mime_type or "video/mp4"
        file_name = msg.video.file_name or "video"
    elif msg.video_note:
        file_type = "video_note"
        mime_type = "video/mp4"  # Telegram video notes are always MP4
        file_name = "video_note"
    elif msg.audio:
        file_type = "audio"
        mime_type = msg.audio.mime_type or "audio/mpeg"
        file_name = msg.audio.file_name or "audio"
    elif msg.voice:
        file_type = "voice"
        mime_type = "audio/ogg"  # Telegram voice notes are always OGG
        file_name = "voice_message"
    elif msg.photo:
        file_type = "photo"
        mime_type = "image/jpeg"  # Telegram photos are always JPEG
        file_name = "photo"

    # Get file size
    file_size = getattr(getattr(msg, file_type), 'file_size', 0)

    # Get the most likely extension from MIME type
    ext = mimetypes.guess_extension(mime_type or "") or ".bin"
    
    # Clean up extension (remove leading dot and lowercase)
    ext = ext.lstrip('.').lower()
    
    # Special cases for known Telegram formats
    if file_type == "voice":
        ext = "ogg"
    elif file_type == "video_note":
        ext = "mp4"
    elif file_type == "photo":
        ext = "jpg"

    # If we have a filename, try to get extension from it
    if hasattr(getattr(msg, file_type), 'file_name'):
        original_name = getattr(msg, file_type).file_name
        if original_name:
            try:
                original_ext = Path(original_name).suffix.lstrip('.').lower()
                if original_ext:  # Only use if we found an extension
                    ext = original_ext
            except:
                pass

    file = await msg.copy(
        chat_id=Telegram.CHANNEL_ID,
        caption=f'||{secret_code}/{sender_id}||'
    )
    file_id = file.id
    
    # Generate links with extension
    dl_link = f'{Server.BASE_URL}/dl/{file_id}?code={secret_code}.{ext}'
    stream_link = f'{Server.BASE_URL}/stream/{file_id}?code={secret_code}'
    
    formatted_message = MediaLinkText.format(
        file_name=file_name,
        file_size=humanbytes(file_size),
        dl_link=dl_link,
        stream_link=stream_link
    )
    
    file_message = FileLinkText.format(
        file_name=file_name,
        file_size=humanbytes(file_size),
        dl_link=dl_link
    )

    if (msg.document and 'video' in (mime_type or "")) or msg.video:
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