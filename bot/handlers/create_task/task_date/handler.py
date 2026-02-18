from datetime import datetime

from aiogram.types import Message
from aiogram_dialog import DialogManager, StartMode
from aiogram_dialog.widgets.input import MessageInput

from states.start_state import StartStateGroup


async def date_handler(
    message: Message, _: MessageInput, dialog_manager: DialogManager
):
    date_str = message.text.strip()
    try:
        date = datetime.fromisoformat(date_str)
    except ValueError:
        dialog_manager.dialog_data["result"] = (
            "❌ Некорректный формат даты. Используйте YYYY-MM-DD или YYYY-MM-DDTHH:MM:SS"
        )
        await dialog_manager.switch_to(StartStateGroup.start)
        return

    dialog_manager.dialog_data["date"] = date_str
    await dialog_manager.switch_to(StartStateGroup.createTaskTags)
