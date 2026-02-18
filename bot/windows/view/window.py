from aiogram_dialog.widgets.kbd import Button, Row
from aiogram_dialog import Window
from aiogram_dialog.widgets.text import Const, Format

from formatters.task_text.formatter import TasksTextFormatter
from handlers.get_tasks.buttons.handler import (
    prev_page_handler,
    next_page_handler,
    go_home_handler,
)
from states.start_state import StartStateGroup

from formatters.result.formatter import ResultFormatter

tasks_window = Window(
    ResultFormatter("Выберите действиe"),
    TasksTextFormatter(),
    Row(
        Button(Const("⬅ Назад"), id="prev_page", on_click=prev_page_handler),
        Button(Const("➡️ Вперёд"), id="next_page", on_click=next_page_handler),
        Button(Const("🏠 Главная"), id="return", on_click=go_home_handler),
    ),
    state=StartStateGroup.viewTasks,
)
