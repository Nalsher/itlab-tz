from aiogram.types import Message
from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.input import MessageInput

from states.start_state import StartStateGroup


async def title_handler(
    message: Message, _: MessageInput, dialog_manager: DialogManager
):
    title = message.text.strip()
    if not title:
        dialog_manager.dialog_data["result"] = (
            "❌ Title не может быть пустым. Попробуйте снова."
        )
        await dialog_manager.reset()
        return
    if len(title) > 128:
        dialog_manager.dialog_data["result"] = (
            "❌ Title слишком длинный (макс 128 символов)."
        )
        await dialog_manager.switch_to(StartStateGroup.start)
        return

    dialog_manager.dialog_data["title"] = title
    await dialog_manager.switch_to(StartStateGroup.createTaskDescription)
