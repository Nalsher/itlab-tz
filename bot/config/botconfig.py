import os
from aiogram import Bot
from dotenv import load_dotenv

load_dotenv()


def botFabric() -> Bot:
    bot_token = os.getenv("TELEGRAM_TOKEN")
    bot = Bot(bot_token)
    return bot
