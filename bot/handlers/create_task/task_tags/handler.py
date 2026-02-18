import asyncio
import os

import aiohttp
from aiogram.types import Message
from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.input import MessageInput

from states.start_state import StartStateGroup


async def tags_handler(
    message: Message, _: MessageInput, dialog_manager: DialogManager
):
    tags = [t.strip() for t in message.text.split(",") if t.strip()]
    if not tags:
        dialog_manager.dialog_data["result"] = (
            "❌ Теги не могут быть пустыми. Отправьте через запятую."
        )
        await dialog_manager.switch_to(StartStateGroup.start)
        return

    title = dialog_manager.dialog_data.get("title")
    description = dialog_manager.dialog_data.get("description")
    date = dialog_manager.dialog_data.get("date")

    url = os.getenv("BACKEND_URL") + "/api/task/"
    headers = {"Chat-Id": str(message.chat.id)}
    payload = {
        "title": title,
        "description": description,
        "due_date": date,
        "tags": tags,
    }

    async with aiohttp.ClientSession() as session:
        try:
            async with session.post(
                url, headers=headers, json=payload, timeout=10
            ) as response:
                if response.status == 201:
                    dialog_manager.dialog_data["result"] = "✅ Таска успешно создана"
                elif response.status == 400:
                    data = await response.json()
                    dialog_manager.dialog_data["result"] = (
                        f"❌ Ошибка создания таски: {data.get('error', 'Неверные данные')}"
                    )
                else:
                    dialog_manager.dialog_data["result"] = (
                        f"❌ Ошибка сервера: {response.status}"
                    )
        except aiohttp.ClientError as e:
            dialog_manager.dialog_data["result"] = f"❌ Ошибка сети: {str(e)}"
        except asyncio.TimeoutError:
            dialog_manager.dialog_data["result"] = (
                "❌ Таймаут при соединении с сервером"
            )

    await dialog_manager.switch_to(StartStateGroup.start)
