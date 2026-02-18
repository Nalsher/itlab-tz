from aiogram_dialog import Window
from aiogram_dialog.widgets.input import MessageInput
from aiogram_dialog.widgets.text import Const, Format
from aiogram_dialog.widgets.kbd import Cancel

from handlers.create_task.task_date.handler import date_handler
from states.start_state import StartStateGroup

from formatters.result.formatter import ResultFormatter

create_date_window = Window(
    ResultFormatter("Отправьте date задачи"),
    # Const("Отправьте date задачи"),
    MessageInput(date_handler),
    Cancel(Const("Отмена")),
    state=StartStateGroup.createTaskDueDate,
)
