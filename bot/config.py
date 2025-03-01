from os import environ as env

class Telegram:
    API_ID = int(env.get("TELEGRAM_API_ID", 12345))
    API_HASH = env.get("TELEGRAM_API_HASH", "xyz")
    OWNER_ID = [int(x) for x in env.get("OWNER_ID", "5530237028").split()]
    ALLOWED_USER_IDS = env.get("ALLOWED_USER_IDS", "").split()
    BOT_USERNAME = env.get("TELEGRAM_BOT_USERNAME", "xxxx_streambot")
    BOT_TOKEN = env.get("TELEGRAM_BOT_TOKEN", "1234567:xyz")
    CHANNEL_ID = int(env.get("TELEGRAM_CHANNEL_ID", -1002391230632))
    SECRET_CODE_LENGTH = int(env.get("SECRET_CODE_LENGTH", 10))

class Server:
    BASE_URL = env.get("BASE_URL", "https://kawaiimizo-maakichu.hf.space")
    BIND_ADDRESS = env.get("BIND_ADDRESS", "0.0.0.0")
    PORT = int(env.get("PORT", 7860))

# Suppose PICS is defined as a string of links separated by spaces:
PICS = env.get("PICS", "https://envs.sh/0Uw.jpg https://envs.sh/0Uq.jpg https://envs.sh/0U0.jpg https://envs.sh/0UW.jpg https://envs.sh/0UI.jpg https://telegra.ph/file/3d0fac76ab59a4ef83b3a.jpg https://i.imgur.com/byGIN5S.jpg https://telegra.ph/file/d9b391fa763286dea1c38.jpg")

# LOGGING CONFIGURATION
LOGGER_CONFIG_JSON = {
    'version': 1,
    'formatters': {
        'default': {
            'format': '[%(asctime)s][%(name)s][%(levelname)s] -> %(message)s',
            'datefmt': '%d/%m/%Y %H:%M:%S'
        },
    },
    'handlers': {
        'file_handler': {
            'class': 'logging.FileHandler',
            'filename': 'event-log.txt',
            'formatter': 'default'
        },
        'stream_handler': {
            'class': 'logging.StreamHandler',
            'formatter': 'default'
        }
    },
    'loggers': {
        'uvicorn': {
            'level': 'INFO',
            'handlers': ['file_handler', 'stream_handler']
        },
        'uvicorn.error': {
            'level': 'WARNING',
            'handlers': ['file_handler', 'stream_handler']
        },
        'bot': {
            'level': 'INFO',
            'handlers': ['file_handler', 'stream_handler']
        },
        'hydrogram': {
            'level': 'INFO',
            'handlers': ['file_handler', 'stream_handler']
        }
    }
}
