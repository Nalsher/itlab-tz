import os

from aiogram import Bot
from celery import shared_task
from itlabdjango.celery import app
from dotenv import load_dotenv
import asyncio

load_dotenv()


@shared_task
def due_date_notify(chat_id: str, task_title: str):
    bot = Bot(token=os.getenv("TELEGRAM_TOKEN"))
    message_text = f"Срок выполнения задачи {task_title} - сегодня"
    asyncio.run(bot.send_message(chat_id=chat_id, text=message_text))
