from aiogram_dialog import Window
from aiogram_dialog.widgets.input import MessageInput
from aiogram_dialog.widgets.text import Const, Format
from aiogram_dialog.widgets.kbd import Cancel

from handlers.create_task.task_description.handler import description_handler
from states.start_state import StartStateGroup

from formatters.result.formatter import ResultFormatter

create_description_window = Window(
    ResultFormatter("Отправьте description задачи"),
    # Const("Отправьте description задачи"),
    MessageInput(description_handler),
    Cancel(Const("Отмена")),
    state=StartStateGroup.createTaskDescription,
)
