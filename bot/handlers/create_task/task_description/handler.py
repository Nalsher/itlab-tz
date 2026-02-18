from aiogram.types import Message
from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.input import MessageInput

from states.start_state import StartStateGroup


async def description_handler(
    message: Message, _: MessageInput, dialog_manager: DialogManager
):
    description = message.text.strip()
    if not description:
        dialog_manager.dialog_data["result"] = "❌ Description не может быть пустым."
        await dialog_manager.switch_to(StartStateGroup.start)
        return

    dialog_manager.dialog_data["description"] = description
    await dialog_manager.switch_to(StartStateGroup.createTaskDueDate)
