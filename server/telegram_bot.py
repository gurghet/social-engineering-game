import os
from telegram import Bot
from telegram.error import TelegramError
import asyncio
from functools import wraps
from config import load_env
from datetime import datetime

load_env()

TELEGRAM_BOT_TOKEN = os.getenv("JANET_SEG_BOT_TOKEN")
CHAT_ID = os.getenv("JANET_SEG_BOT_CHAT_ID")

if not TELEGRAM_BOT_TOKEN or not CHAT_ID:
    raise ValueError("Missing required environment variables: JANET_SEG_BOT_TOKEN or JANET_SEG_BOT_CHAT_ID")

bot = Bot(token=TELEGRAM_BOT_TOKEN)

def async_to_sync(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            loop = asyncio.get_event_loop()
        except RuntimeError:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
        return loop.run_until_complete(func(*args, **kwargs))
    return wrapper

@async_to_sync
async def send_message(message: str) -> bool:
    """Send a message to the configured Telegram chat.
    
    Args:
        message (str): The message to send
        
    Returns:
        bool: True if message was sent successfully, False otherwise
    """
    try:
        await bot.send_message(chat_id=CHAT_ID, text=message)
        return True
    except TelegramError as e:
        print(f"Failed to send message to Telegram: {e}")
        return False

def format_game_message(event_type: str, content: str) -> str:
    """Format a game event message for Telegram.
    
    Args:
        event_type (str): Type of event (e.g., 'GAME_ROUND')
        content (str): The content to format
        
    Returns:
        str: Formatted message for Telegram
    """
    divider = "=" * 40
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    return f"""🎮 Social Engineering Game - {event_type}
⏰ {timestamp}
{divider}

{content}

{divider}"""
