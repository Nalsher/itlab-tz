from aiogram_dialog import Window, StartMode
from aiogram_dialog.widgets.text import Const, Format
from aiogram_dialog.widgets.kbd import Start, Button

from handlers.get_tasks.buttons.handler import show_tasks_page
from states.start_state import StartStateGroup

from formatters.result.formatter import ResultFormatter

start_window = Window(
    ResultFormatter("Выберите действиe"),
    # Const("Выберите действие"),
    Button(
        Const("➕ Создать таску"),
        id="create_task",
        on_click=lambda callback, button, manager: manager.switch_to(
            StartStateGroup.createTaskTitle
        ),
    ),
    Button(
        Const("Получить текущие таски"),
        id="get_tasks",
        on_click=show_tasks_page,
    ),
    Start(
        Const("Зарегистрировать токен"),
        id="registry",
        state=StartStateGroup.registry,
        mode=StartMode.RESET_STACK,
    ),
    state=StartStateGroup.start,
)
