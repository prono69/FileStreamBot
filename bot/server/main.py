from quart import Blueprint, Response, request, render_template, redirect, jsonify
from math import ceil
import time
from re import match as re_match
from .error import abort
from bot import TelegramBot, StartTime, utils
from bot.config import Telegram, Server
from bot.modules.telegram import get_message, get_file_properties

bp = Blueprint('main', __name__)
CHUNK_SIZE_MB = 4  # Default to 4MB chunks

@bp.route('/')
async def home():
    system_info = utils.get_system_info()
    # Pass system_info to the template
    return await render_template("index.html", system_info=system_info)


@bp.route('/bot')
async def bot():
    return redirect(f'https://t.me/{Telegram.BOT_USERNAME}')
    

@bp.route('/status')
async def status():
    return jsonify({
        "status": "running",
        "uptime": utils.get_readable_time(time.time() - StartTime),
        "telegram_bot": "@" + Telegram.BOT_USERNAME,
    })


@bp.route('/health')
async def health():
    return jsonify({
        "message": "running",
    })


@bp.route('/dl/<int:file_id>', methods=['GET', 'POST', 'HEAD'])
async def transmit_file(file_id):
    file = await get_message(file_id) or abort(404)
    code = request.args.get('code') or abort(401)
    range_header = request.headers.get('Range')

    if code != file.caption.split('/')[0]:
        abort(403)

    file_name, file_size, mime_type = get_file_properties(file)

    start = 0
    end = file_size - 1
    chunk_size = 1 * 1024 * 1024  # 1 MB

    if range_header:
        range_match = re_match(r'bytes=(\d+)-(\d*)', range_header)
        if range_match:
            start = int(range_match.group(1))
            end = int(range_match.group(2)) if range_match.group(2) else file_size - 1
            if start > end or start >= file_size:
                abort(416, 'Requested range not satisfiable')
        else:
            abort(400, 'Invalid Range header')

    offset_chunks = start // chunk_size
    total_bytes_to_stream = end - start + 1
    chunks_to_stream = ceil(total_bytes_to_stream / chunk_size)

    content_length = total_bytes_to_stream
    headers = {
        'Content-Type': mime_type,
        'Content-Disposition': f'attachment; filename={file_name}',
        'Content-Range': f'bytes {start}-{end}/{file_size}',
        'Accept-Ranges': 'bytes',
        'Content-Length': str(content_length),
    }
    status_code = 206 if range_header else 200

    async def file_stream():
        bytes_streamed = 0
        chunk_index = 0
        async for chunk in TelegramBot.stream_media(
            file,
            offset=offset_chunks,
            limit=chunks_to_stream,
        ):
            if chunk_index == 0: # Trim the first chunk if necessary
                trim_start = start % chunk_size
                if trim_start > 0:
                    chunk = chunk[trim_start:]

            remaining_bytes = content_length - bytes_streamed
            if remaining_bytes <= 0:
                break

            if len(chunk) > remaining_bytes: # Trim the last chunk if necessary
                chunk = chunk[:remaining_bytes]

            yield chunk
            bytes_streamed += len(chunk)
            chunk_index += 1

    return Response(file_stream(), headers=headers, status=status_code)

@bp.route('/stream/<int:file_id>', methods=['GET', 'POST', 'HEAD'])
async def stream_file(file_id):
    code = request.args.get('code') or abort(401)
    return await render_template('player.html', mediaLink=f'{Server.BASE_URL}/dl/{file_id}?code={code}')


@bp.route('/ssgen/<int:file_id>', methods=['GET', 'POST', 'HEAD'])
async def transmit_file_without_code(file_id):
    file = await get_message(file_id) or abort(404)
    range_header = request.headers.get('Range')

    file_name, file_size, mime_type = get_file_properties(file)
    chunk_size = min(file_size // 50, CHUNK_SIZE_MB * 1024 * 1024)  # Adaptive chunk size
    start = 0
    end = file_size - 1

    if range_header:
        range_match = re_match(r'bytes=(\d+)-(\d*)', range_header)
        if range_match:
            start = int(range_match.group(1))
            end = int(range_match.group(2)) if range_match.group(2) else file_size - 1
            if start > end or start >= file_size:
                abort(416, 'Requested range not satisfiable')
        else:
            abort(400, 'Invalid Range header')

    offset_chunks = start // chunk_size
    total_bytes_to_stream = end - start + 1
    chunks_to_stream = ceil(total_bytes_to_stream / chunk_size)

    content_length = total_bytes_to_stream
    headers = {
        'Content-Type': mime_type,
        'Content-Disposition': f'attachment; filename={file_name}',
        'Content-Range': f'bytes {start}-{end}/{file_size}',
        'Accept-Ranges': 'bytes',
        'Content-Length': str(content_length),
    }
    status_code = 206 if range_header else 200

    async def file_stream():
        """Streams the file efficiently using parallel chunk fetching."""
        bytes_streamed = 0
        chunk_index = 0

        async def fetch_chunk(offset, limit):
            """Fetches a chunk of the file asynchronously."""
            async for chunk in TelegramBot.stream_media(file, offset=offset, limit=limit):
                return chunk
            return None

        chunk_tasks = [
            fetch_chunk(offset_chunks + i, 1) for i in range(chunks_to_stream)
        ]
        fetched_chunks = await asyncio.gather(*chunk_tasks)

        for i, chunk in enumerate(fetched_chunks):
            if chunk_index == 0:  # Trim the first chunk if necessary
                trim_start = start % chunk_size
                if trim_start > 0:
                    chunk = chunk[trim_start:]

            remaining_bytes = content_length - bytes_streamed
            if remaining_bytes <= 0:
                break

            if len(chunk) > remaining_bytes:  # Trim the last chunk if necessary
                chunk = chunk[:remaining_bytes]

            yield chunk
            bytes_streamed += len(chunk)
            chunk_index += 1

    return Response(file_stream(), headers=headers, status=status_code)
    

@bp.route('/noauth/<int:file_id>', methods=['GET', 'POST', 'HEAD'])
async def transmit_file_without(file_id):
    file = await get_message(file_id) or abort(404)
    range_header = request.headers.get('Range')

    file_name, file_size, mime_type = get_file_properties(file)

    # Defaults for full file
    start = 0
    end = file_size - 1

    # Use adaptive chunk size: up to 4 MB (or smaller if the file is small)
    max_chunk_size = 4 * 1024 * 1024  # 4 MB
    chunk_size = min(max_chunk_size, file_size)

    if range_header:
        range_match = re_match(r'bytes=(\d+)-(\d*)', range_header)
        if range_match:
            start = int(range_match.group(1))
            end = int(range_match.group(2)) if range_match.group(2) else file_size - 1
            if start > end or start >= file_size:
                abort(416, 'Requested range not satisfiable')
        else:
            abort(400, 'Invalid Range header')

    total_bytes_to_stream = end - start + 1

    # Determine the starting chunk index and number of chunks needed.
    offset_chunks = start // chunk_size
    chunks_to_stream = int(ceil(total_bytes_to_stream / chunk_size))

    headers = {
        'Content-Type': mime_type,
        'Content-Disposition': f'attachment; filename={file_name}',
        'Content-Range': f'bytes {start}-{end}/{file_size}',
        'Accept-Ranges': 'bytes',
        'Content-Length': str(total_bytes_to_stream),
    }
    status_code = 206 if range_header else 200

    async def fetch_chunk(chunk_idx):
        """
        Fetch a single chunk using TelegramBot.stream_media.
        The offset is measured in chunk units.
        """
        async for chunk in TelegramBot.stream_media(file, offset=offset_chunks + chunk_idx, limit=1):
            return chunk

    async def file_stream():
        # Launch concurrent tasks for all chunks needed.
        tasks = [asyncio.create_task(fetch_chunk(i)) for i in range(chunks_to_stream)]
        all_chunks = await asyncio.gather(*tasks)

        # Apply trimming to the first and last chunks so that the combined bytes equal total_bytes_to_stream.
        # Trim the first chunk if needed.
        first_chunk = all_chunks[0][start % chunk_size:]
        if chunks_to_stream == 1:
            # Only one chunk: yield exactly total_bytes_to_stream bytes.
            yield first_chunk[:total_bytes_to_stream]
        else:
            yield first_chunk
            for chunk in all_chunks[1:-1]:
                yield chunk
            # For the last chunk, compute how many bytes remain after the previous chunks.
            bytes_yielded = len(first_chunk) + sum(len(chunk) for chunk in all_chunks[1:-1])
            remaining_bytes = total_bytes_to_stream - bytes_yielded
            last_chunk = all_chunks[-1][:remaining_bytes]
            yield last_chunk

    return Response(file_stream(), headers=headers, status=status_code)
