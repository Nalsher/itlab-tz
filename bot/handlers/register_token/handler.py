import os

import aiohttp
from aiogram.types import Message
from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.input import MessageInput

from states.start_state import StartStateGroup


async def token_handler(
    message: Message, _: MessageInput, dialog_manager: DialogManager
):
    token = message.text.strip()

    dialog_manager.dialog_data["token"] = token

    async with aiohttp.ClientSession() as session:
        try:
            async with session.post(
                os.getenv("BACKEND_URL") + "/api/telegram/",
                json={"token": token, "chat_id": message.chat.id},
            ) as response:
                if response.status == 200:
                    dialog_manager.dialog_data["result"] = (
                        "Токен успешно зарегистрирован"
                    )
                else:
                    dialog_manager.dialog_data["result"] = "Неверный токен"
        except Exception as e:
            dialog_manager.dialog_data["result"] = "Ошибка отправки токена"

    await dialog_manager.switch_to(StartStateGroup.start)
