from aiogram.types import CallbackQuery
from aiogram_dialog import DialogManager

from handlers.get_tasks.handler import fetch_tasks_page
from states.start_state import StartStateGroup


async def show_tasks_page(callback: CallbackQuery, widget, manager: DialogManager):
    page = manager.dialog_data.get("tasks_page", 0)
    chat_id = callback.message.chat.id

    data = await fetch_tasks_page(page, chat_id)
    manager.dialog_data["tasks"] = data.get("results")
    manager.dialog_data["tasks_page"] = data.get("current_page") - 1
    manager.dialog_data["tasks"] = data.get("results", [])
    manager.dialog_data["next_page_exists"] = data.get("next") is not None
    manager.dialog_data["prev_page_exists"] = data.get("previous") is not None

    await manager.switch_to(StartStateGroup.viewTasks)


async def next_page_handler(callback: CallbackQuery, widget, manager: DialogManager):
    if manager.dialog_data.get("next_page_exists"):
        manager.dialog_data["tasks_page"] += 1
        await show_tasks_page(callback, widget, manager)


async def prev_page_handler(callback: CallbackQuery, widget, manager: DialogManager):
    if (
        manager.dialog_data.get("prev_page_exists")
        and manager.dialog_data["tasks_page"] > 0
    ):
        manager.dialog_data["tasks_page"] -= 1
        await show_tasks_page(callback, widget, manager)


async def go_home_handler(callback: CallbackQuery, widget, manager: DialogManager):
    await manager.switch_to(StartStateGroup.start)
